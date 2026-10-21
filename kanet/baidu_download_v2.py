#!/usr/bin/env python3
"""
Attempt to download pretrained model from Baidu Pan using alternative methods.
"""
import requests
import os
import sys
import json
from urllib.parse import quote

SHAREID = "41157009423"
UK = "3661203548"
PWD = "n2k4"
OUTPUT_DIR = "src/KA_Net_repo/testcode"

def attempt_direct_download():
    """Try direct download approaches."""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': f'https://pan.baidu.com/s/1HETnxLCTxjHRsBg2STwsHQ',
    })
    
    # Try accessing share page with password in cookie
    urls_to_try = [
        f"https://pan.baidu.com/api/sharedownload?shareid={SHAREID}&uk={UK}&web=1&pwd={PWD}",
        f"https://pan.baidu.com/api/share/list?shareid={SHAREID}&uk={UK}",
    ]
    
    for url in urls_to_try:
        try:
            print(f"[*] Trying: {url}")
            resp = session.get(url, timeout=10, cookies={'BDUSS': '', 'PSTM': ''})
            print(f"    Status: {resp.status_code}")
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    print(f"    Response: {json.dumps(data, indent=2)[:200]}")
                    if data.get('errno') == 0:
                        print("[+] Got valid response!")
                        return data
                except:
                    pass
        except Exception as e:
            print(f"    Error: {e}")
    
    return None

def suggest_alternative_sources():
    """List alternative ways to get the model."""
    print("\n" + "="*80)
    print("ALTERNATIVE APPROACHES TO GET THE PRETRAINED MODEL")
    print("="*80)
    print("\n1. MANUAL DOWNLOAD (RECOMMENDED)")
    print("   - Open browser: https://pan.baidu.com/s/1HETnxLCTxjHRsBg2STwsHQ")
    print("   - Enter code: n2k4")
    print("   - Download the file")
    print("   - Place in: src\\KA_Net_repo\\testcode\\")
    
    print("\n2. CONTACT AUTHOR")
    print("   - GitHub: https://github.com/fyxnl/KA_Net")
    print("   - Request model via issues or email")
    
    print("\n3. ALTERNATIVE MODEL SOURCES")
    print("   - Check if paper provides supplementary materials")
    print("   - Look for pre-trained models from citations")
    
    print("\n4. TRAIN YOUR OWN MODEL")
    print("   - Check if KA_Net repo has training code")
    print("   - Use synthesized data or public dehazing datasets")
    
    print("\n" + "="*80)
    print("ONCE YOU HAVE THE MODEL FILE (.pk):")
    print("="*80)
    print("""
# Copy the model file to testcode folder
Copy-Item "C:\\path\\to\\downloaded\\model.pk" "src\\KA_Net_repo\\testcode\\model.pk"

# Create conda environment
conda env create -f src\\KA_Net_repo\\environment.yml -n ka_net
conda activate ka_net

# Run the test
python src\\KA_Net_repo\\testcode\\KA_net_test.py \\
  --model src\\KA_Net_repo\\testcode\\model.pk \\
  --test_dir src\\KA_Net_repo\\input \\
  --out_dir src\\KA_Net_repo\\results \\
  --device cpu
""")
    print("="*80)

def main():
    print("[*] Attempting alternative Baidu download methods...")
    
    result = attempt_direct_download()
    
    if result is None:
        print("\n[-] All automated download methods failed")
        print("[-] Baidu Pan requires interactive authentication (browser login, captcha)")
        suggest_alternative_sources()
        return 1
    
    print("[+] Download successful!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
