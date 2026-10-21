import sys
import os
import traceback

script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

def main():
    try:
        from LD_model1 import Dehaze
        import torch

        device = torch.device('cpu')
        net = Dehaze(3, 3).to(device)
        net.eval()

        x = torch.randn(1, 3, 256, 256, device=device)
        with torch.no_grad():
            out, z = net(x)

        print('Forward pass succeeded.')
        print('out shape:', getattr(out, 'shape', None))
        print('z shape:', getattr(z, 'shape', None))
    except Exception:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
