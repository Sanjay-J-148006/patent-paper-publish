#!/usr/bin/env python3
import requests
import json
import os
import sys
from pathlib import Path

# Baidu share info extracted from the share page
SHAREID = "41157009423"
UK = "3661203548"
PWD = "n2k4"  # extraction code
OUTPUT_DIR = "src/KA_Net_repo/testcode"

def create_session():
    """Create a requests session with proper headers."""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    return session

def get_share_file_list(session):
    """Fetch the list of files in the share using the API."""
    url = f"https://pan.baidu.com/api/sharedownload"
    params = {
        'shareid': SHAREID,
        'uk': UK,
        'sign': '',
        'timestamp': '',
        'bdstoken': '',
        'web': '1'
    }
    try:
        # First, check if we need to provide the extraction code
        print("[*] Attempting to fetch share file list...")
        resp = session.get(url, params=params, timeout=10)
        print(f"[*] Response status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"[*] Response data: {data}")
            return data
    except Exception as e:
        print(f"[-] Error fetching file list: {e}")
    return None

def verify_pwd(session):
    """Verify the extraction password."""
    url = f"https://pan.baidu.com/api/share/shareid/{SHAREID}/verify"
    data = {
        'pwd': PWD,
        'vcode': '',
        'vcode_str': ''
    }
    try:
        print("[*] Verifying extraction code...")
        resp = session.post(url, data=data, timeout=10)
        print(f"[*] Verify response status: {resp.status_code}")
        print(f"[*] Verify response: {resp.text}")
        if resp.status_code == 200:
            result = resp.json()
            if result.get('errno') == 0:
                print("[+] Extraction code verified successfully")
                return True
    except Exception as e:
        print(f"[-] Error verifying pwd: {e}")
    return False

def download_via_api(session):
    """Try to download using the share API."""
    print("[*] Attempting API-based download...")
    # This is a complex process that may require token handling
    # The actual implementation would need to reverse-engineer Baidu's API
    print("[-] API-based download requires complex token/session handling")
    return False

def fallback_message():
    """If all automated methods fail, provide manual download instructions."""
    print("\n" + "="*70)
    print("AUTOMATED DOWNLOAD FAILED - MANUAL DOWNLOAD REQUIRED")
    print("="*70)
    print("\nPlease download the file manually:")
    print(f"  URL: https://pan.baidu.com/s/1HETnxLCTxjHRsBg2STwsHQ")
    print(f"  Extraction Code: {PWD}")
    print(f"\nAfter downloading, place the file in:")
    print(f"  {os.path.abspath(OUTPUT_DIR)}/")
    print("\nThen run the test with:")
    print(f"  python {OUTPUT_DIR}/KA_net_test.py --model {OUTPUT_DIR}/<model_filename.pk> --test_dir src/KA_Net_repo/input --out_dir src/KA_Net_repo/results --device cpu")
    print("="*70)

def main():
    print("[*] Starting Baidu share download...")
    print(f"[*] Share ID: {SHAREID}")
    print(f"[*] UK: {UK}")
    print(f"[*] Extraction Code: {PWD}")
    print(f"[*] Output Directory: {OUTPUT_DIR}")
    
    session = create_session()
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Attempt various methods
    if verify_pwd(session):
        if download_via_api(session):
            print("[+] Download successful!")
            return 0
    
    # If we get here, automated download failed
    fallback_message()
    return 1

if __name__ == "__main__":
    sys.exit(main())
