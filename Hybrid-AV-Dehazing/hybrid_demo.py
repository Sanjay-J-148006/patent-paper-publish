import cv2
import torch
import numpy as np
from kanet_kernel import KernelAttention, load_ka_weights
from orama_wrapper import OramaProcessor

def process_single_image():
    # Paths based on your structure
    input_img = 'input/image.jpg'  # Your attached image
    output_orama = 'output/orama_dehazed.jpg'
    output_final = 'output/hybrid_dehazed.jpg'
    
    # Initialize models
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    orama = OramaProcessor()
    ka_module = KernelAttention(in_channels=3).to(device)
    ka_module = load_ka_weights(ka_module)
    ka_module.eval()
    
    # Load and process image
    img = cv2.imread(input_img)
    print(f"Processing {input_img}...")
    
    # Step 1: Orama dehazing
    orama_result = orama.dehaze_image(img)
    cv2.imwrite(output_orama, orama_result)
    print(f"Orama saved: {output_orama}")
    
    # Step 2: KA-Net Kernel Attention refinement
    img_tensor = torch.from_numpy(cv2.cvtColor(orama_result, cv2.COLOR_BGR2RGB)).float()
    img_tensor = img_tensor.permute(2,0,1).unsqueeze(0).to(device) / 255.0
    
    with torch.no_grad():
        final_result = ka_module(img_tensor)
        final_result = final_result.squeeze(0).permute(1,2,0).cpu().numpy() * 255.0
        final_result = np.clip(final_result, 0, 255).astype(np.uint8)
        final_result = cv2.cvtColor(final_result, cv2.COLOR_RGB2BGR)
    
    cv2.imwrite(output_final, final_result)
    print(f"Hybrid result saved: {output_final}")

if __name__ == "__main__":
    process_single_image()
