#!/usr/bin/env python3
import requests
import re
import os
from datetime import datetime

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H")

def download_page(url, headers=None):
    try:
        response = requests.get(url, timeout=30, headers=headers or {})
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return ""

def extract_hashes_sha256(text):
    hashes = set()
    patterns = [
        r'\b[a-fA-F0-9]{64}\b',
    ]
    for pattern in patterns:
        for match in re.findall(pattern, text):
            if len(match) == 64:
                hashes.add(match.lower())
    return list(hashes)

def extract_hashes_md5(text):
    hashes = set()
    patterns = [
        r'\b[a-fA-F0-9]{32}\b',
    ]
    for pattern in patterns:
        for match in re.findall(pattern, text):
            if len(match) == 32:
                hashes.add(match.lower())
    return list(hashes)

def extract_ips(text):
    ips = set()
    pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    for match in re.findall(pattern, text):
        parts = match.split('.')
        if len(parts) == 4 and all(0 <= int(p) <= 255 for p in parts if p.isdigit()):
            ips.add(match)
    return list(ips)

def save_to_file(filepath, data):
    if not data:
        print(f"No data to save to {filepath}")
        return False
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    content = '\n'.join(sorted(set(data))) + '\n'
    
    if len(content.encode()) > MAX_FILE_SIZE:
        parts = []
        current = []
        current_size = 0
        for item in sorted(set(data)):
            item_size = len(item.encode()) + 1
            if current_size + item_size > MAX_FILE_SIZE:
                parts.append(current)
                current = []
                current_size = 0
            current.append(item)
            current_size += item_size
        if current:
            parts.append(current)
        
        base_path = filepath.replace('.txt', '')
        for i, part in enumerate(parts, 1):
            part_path = f"{base_path}_part{i}.txt"
            with open(part_path, 'w') as f:
                f.write('\n'.join(sorted(part)) + '\n')
            print(f"Saved {len(part)} items to {part_path}")
        return True
    else:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Saved {len(data)} items to {filepath}")
        return True

def download_triage():
    print("Downloading Triage...")
    url = "https://tria.ge/reports/public?limit=1000"
    text = download_page(url)
    hashes = extract_hashes_sha256(text)
    print(f"Found {len(hashes)} hashes from Triage")
    return hashes

def download_vxvault():
    print("Downloading VX Vault...")
    url = "http://vxvault.net/ViriList.php?s=0&m=100"
    text = download_page(url)
    hashes = extract_hashes_md5(text)
    ips = extract_ips(text)
    print(f"Found {len(hashes)} hashes and {len(ips)} IPs from VX Vault")
    return hashes, ips

def download_valhalla():
    print("Downloading Valhalla...")
    url = "https://valhalla.nextron-systems.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    text = download_page(url, headers)
    hashes = extract_hashes_sha256(text)
    print(f"Found {len(hashes)} hashes from Valhalla")
    return hashes

def main():
    ts = get_timestamp()
    base_dir = "hashes"
    
    hashes_triage = download_triage()
    if hashes_triage:
        save_to_file(f"{base_dir}/triage/hashes_triage_{ts}.txt", hashes_triage)
    
    hashes_vx, ips_vx = download_vxvault()
    if hashes_vx:
        save_to_file(f"{base_dir}/vxvault/hashes_vxvault_{ts}.txt", hashes_vx)
    if ips_vx:
        save_to_file(f"{base_dir}/vxvault/ips_vxvault_{ts}.txt", ips_vx)
    
    hashes_valhalla = download_valhalla()
    if hashes_valhalla:
        save_to_file(f"{base_dir}/valhalla/hashes_valhalla_{ts}.txt", hashes_valhalla)
    
    print("Done!")

if __name__ == "__main__":
    main()