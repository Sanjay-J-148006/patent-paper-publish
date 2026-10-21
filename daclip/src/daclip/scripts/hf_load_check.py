import torch
p='pretrained/daclip_ViT-B-32-hf.pt'
print('Loading',p)
try:
    obj=torch.load(p,map_location='cpu')
    print('Loaded type:', type(obj))
    if isinstance(obj, dict):
        print('Top keys:', list(obj.keys())[:20])
    else:
        print('Object repr:', repr(obj)[:200])
except Exception as e:
    print('ERROR loading:', e)
    import traceback
    traceback.print_exc()
    raise
