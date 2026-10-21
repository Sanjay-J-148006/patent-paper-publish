import cv2
import torch
import sys
sys.path.append('..')

print("🌙 Nighttime Dehaze Quick Demo")
cap = cv2.VideoCapture(0)  # Webcam

while True:
    ret, frame = cap.read()
    if not ret: break
    
    # Load model (assumes best.pt exists)
    # model = torch.load("results/dehaze/model/best.pt")
    dehazed = frame  # Placeholder - replace with real inference
    
    cv2.imshow("Night Fog → Clear Windshield", dehazed)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("✅ Webcam dehazing demo complete!")
