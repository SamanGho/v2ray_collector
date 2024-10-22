

# Function to replace specific text in links


    # Replacing all occurrences based on the dictionary



import requests
from bs4 import BeautifulSoup
import os
import time
import sys
import base64  # To handle base64 encoding

# Function to extract V2Ray links
def extract_v2ray_links(url, timeout=15, retries=5, retry_delay=8):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                v2ray_links = []

                # Find all divs with the specific class and extract the links
                for div in soup.find_all('div', class_='tgme_widget_message_text js-message_text'):
                    code_tag = div.find('code')
                    if code_tag and code_tag.text.startswith(('vless://', 'vmess://', 'trojan://', 'ss://')):
                        v2ray_links.append(code_tag.text.strip())

                return v2ray_links
            else:
                print(f"Failed to fetch URL: {url} , status code = {response.status_code}")
                return []
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            print(f"Attempt {attempt + 1} failed {url}: {e}")
            attempt += 1
            time.sleep(retry_delay)
    print(f"All {retries} attempts to collect failed for {url}")
    return []

# Function to replace specific text in links
def replace_links(links):
    replacements = {
        "t.me/ConfigsHub": "t.me/V2razy",
        "@v2ray_configs_pool": "@V2razy",
        "t.me/PrivateVPNs":"t.me/V2razy",
        "@VlessConfig":"@V2razy",
        "@DirectVPN":"@V2razy",
        "DailyV2ry" :"@v2razy"

    }

    # Replacing all occurrences based on the dictionary
    updated_links = []
    for link in links:
        for old, new in replacements.items():
            link = link.replace(old, new)
        updated_links.append(link)

    return updated_links

# Function to encode links to base64
def encode_links_to_base64(links):
    encoded_links = []
    for link in links:
        encoded_link = base64.b64encode(link.encode('utf-8')).decode('utf-8')
        encoded_links.append(encoded_link)
    return encoded_links

# Function to save V2Ray links to a file, avoiding duplicates
def save_v2ray_links(links, filename):
    if links:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                existing_links = set(file.read().splitlines())
        else:
            existing_links = set()

        new_links = set(links) - existing_links
        with open(filename, 'a', encoding='utf-8') as file:
            for link in new_links:
                file.write(link + '\n')

def main():
    # Check if the filename is passed as an argument
    if len(sys.argv) < 2:
        print("Error: Filename argument is missing.")
        sys.exit(1)

    filename = sys.argv[1]

    telegram_urls = [
        "https://t.me/s/v2ray_configs_pool",
        "https://t.me/s/ConfigsHUB2",
        "https://t.me/s/PrivateVPNs",
        "https://t.me/s/VlessConfig", 
        "https://t.me/s/DirectVPN",
        "https://t.me/s/FreeV2rays",
        "https://t.me/s/freev2rayssr",
       # "https://t.me/s/DailyV2RY",  fix for it later
        "https://t.me/s/v2ray_outlineir"

    ]

    all_links = []
    for url in telegram_urls:
        links = extract_v2ray_links(url)
        all_links.extend(links)

    # Replace links before saving
    updated_links = replace_links(all_links)

    # Encode links to base64
    base64_links = encode_links_to_base64(updated_links)

    save_v2ray_links(base64_links, filename)

if __name__ == "__main__":
    main()
