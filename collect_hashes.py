#!/usr/bin/env python3
import requests
import re
import os

HASHES_FILE = "hashes/hashes_unicos.txt"

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

def merge_into_file(filepath, data):
    existing = set()
    if os.path.exists(filepath):
        with open(filepath) as f:
            existing = {line.strip() for line in f if line.strip()}
    new = set(data) - existing
    if not new:
        print(f"No new items for {filepath}")
        return
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write('\n'.join(sorted(existing | new)) + '\n')
    print(f"Added {len(new)} new items to {filepath} ({len(existing | new)} total)")

def download_triage():
    print("Downloading Triage...")
    url = "https://tria.ge/reports/public?limit=1000"
    text = download_page(url)
    hashes = extract_hashes_sha256(text)
    print(f"Found {len(hashes)} hashes from Triage")
    return hashes

def download_valhalla():
    print("Downloading Valhalla...")
    url = "https://valhalla.nextron-systems.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    text = download_page(url, headers)
    hashes = extract_hashes_sha256(text)
    print(f"Found {len(hashes)} hashes from Valhalla")
    return hashes

def main():
    hashes_triage = download_triage()
    hashes_valhalla = download_valhalla()

    merge_into_file(HASHES_FILE, hashes_triage + hashes_valhalla)

    print("Done!")

if __name__ == "__main__":
    main()