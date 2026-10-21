"""Download large files from Google Drive using confirmation token flow.
Usage: python download_gdrive.py <file_id> <destination_path>
"""
import sys
import requests

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    # fallback: search in content
    import re
    m = re.search(r"confirm=([0-9A-Za-z_\-]+)", response.text)
    if m:
        return m.group(1)
    return None


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    CHUNK_SIZE = 32768
    total = 0
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                total += len(chunk)
    return total

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python download_gdrive.py <file_id> <destination_path>")
        sys.exit(2)
    file_id = sys.argv[1]
    dest = sys.argv[2]
    print(f"Downloading file id {file_id} to {dest} ...")
    try:
        size = download_file_from_google_drive(file_id, dest)
        print(f"Done. Wrote {size} bytes")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
