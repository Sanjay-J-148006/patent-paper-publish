import sys
import os
from pathlib import Path

# Initialize paths from project root
project_root = Path(__file__).parent
while project_root != project_root.parent:
    if (project_root / "run_model.py").exists():
        break
    project_root = project_root.parent

sys.path.insert(0, str(project_root / 'Windshield-Dehazing-AV' / 'Windshield-Dehazing-AV' / 'Windshield-Dehazing-AV' / 'Windshield-Dehazing-AV' / 'Windshield-Dehazing-AV' / 'src' / 'ka_net' / 'testcode'))
sys.path.insert(0, str(Path(__file__).parent))

# Now import model libraries
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from view_testdata1 import TestData#from test_data_real import TestData
from transweather_model import Transweather
from LD_model1 import Dehaze
import math
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import time
import numpy as np
from Utils import save_image_,PSNR_cal,SSIM_cal,psnr_,ssim_
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.metrics.pairwise import cosine_similarity


def PSNR(img1, img2):
    b,_,_,_=img1.shape
    img1=np.clip(img1,0,255)
    img2=np.clip(img2,0,255)
    mse = np.mean((img1/ 255. - img2/ 255.) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 1
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
def ensure_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
import pathlib
# Use relative paths from project root
project_root = pathlib.Path(__file__).parent.parent.parent.parent.parent
test_dir = project_root / 'paired_data' / 'glow'
test_store = project_root / 'results' / 'ka_net' / 'output'
expname = 'tpami_work/results/mycollection/'
ensure_dir(str(test_store))
device_ids = [Id for Id in range(torch.cuda.device_count())]
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")#11,
model_dir = project_root / 'results' / 'ka_net' / 'model' / 'best.pt'
device='cuda' if torch.cuda.is_available() else 'cpu'
if model_dir.exists():
    ckp = torch.load(str(model_dir), map_location=device)
    net = Dehaze(3,3).to(device)
    net = nn.DataParallel(net)
    net.load_state_dict(ckp['model'])
    net.eval()
else:
    print(f"⚠️  Model not found at {model_dir}")
    print(f"   Creating a dummy model for testing...")
    net = Dehaze(3,3).to(device)
    net = nn.DataParallel(net)
batch_size=1
nyuhaze=False
synTest=True
indoor=False
if not test_dir.exists():
    print(f"⚠️  Test data not found at {test_dir}")
    print(f"   Please provide test images in {test_dir}")
    test_loader = DataLoader([])  # Empty loader
else:
    test_loader=DataLoader(TestData(str(test_dir),synTest,indoor),batch_size=1)
psnr=[]
ssim=[]
start=time.time()

for j,data_ in enumerate(test_loader):
    with torch.no_grad():
        if synTest:
            test_x,test_img_name= data_
            test_x=test_x.to(device)
            b,c,h,w=test_x.size()
            # print(test_x.shape)
            if h%16!=0:
                h0=h%16#550/16=...6
                if h0%2==0:
                    h1=int(h0/2)
                    test_x=test_x[:,:,h1:(h-h1),:]
                else:
                    h1=h0%2
                    test_x=test_x[:,:,h1:(h+h1-h0),:]
            if w%16!=0:
                w0= w% 16
                if w0%2 == 0:
                    w1 = int(w0 / 2)
                    test_x= test_x[:, :, :, w1:(w - w1)]
                else:
                    w1 = w0 % 2
                    test_x = test_x[:, :, :, w1:(w - w0 + w1)]
            predict_y,_=net(test_x)
        else:
            test_x,test_img_name= data_
            test_x=test_x.to(device)
            b,c,h,w=test_x.size()
            if h%16!=0:
                h0=h%16
                if h0%2==0:
                    h1=int(h0/2)
                    test_x=test_x[:,:,h1:(h-h1),:]
                else:
                    h1=h0%2
                    test_x=test_x[:,:,h1:(h+h1-h0),:]
            if w%16!=0:
                w0=w%16
                if w0%2==0:
                    w1=int(w0/2)
                    test_x=test_x[:,:,:,w1:(w-w1)]
                else:
                    w1=w0%2
                    test_x=test_x[:,:,:,w1:(w-w0+w1)]
            try:
                predict_y,_=net(test_x)
            except:
                continue
    save_image_(predict_y,expname,test_img_name)
    # print(j)
end=time.time()-start
print(end)

