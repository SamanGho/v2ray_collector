

import requests
from bs4 import BeautifulSoup
import os
import time
import sys
import base64

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
                for div in soup.find_all('div', class_=lambda x: x and 'tgme_widget_message_text' in x):

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


    }

    # Replacing all occurrences based on the dictionary
    updated_links = []
    for link in links:
        for old, new in replacements.items():
            link = link.replace(old, new)
        updated_links.append(link)

    return updated_links

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

# Function to encode the entire file content to base64
def encode_file_to_base64(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        content = file.read()
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(encoded_content)

def main():
    # Check if the filename is passed as an argument
    if len(sys.argv) < 2:
        print("Error: Filename argument is missing.")
        sys.exit(1)

    filename = sys.argv[1]


    telegram_urls = [
       # "https://t.me/s/v2ray_configs_pool",  forward bzn
        "https://t.me/s/ConfigsHUB",
        "https://t.me/s/PrivateVPNs",
        "https://t.me/s/VlessConfig", 
        "https://t.me/s/DirectVPN",
        "https://t.me/s/FreeV2rays",
        "https://t.me/s/freev2rayssr",
        "https://t.me/s/IP_CF_Config",
       # "https://t.me/s/DailyV2RY",  fix for it later
        "https://t.me/s/v2ray_outlineir"

    ]
    all_links = []
    for url in telegram_urls:
        links = extract_v2ray_links(url)
        all_links.extend(links)

    # Replace links before saving
    updated_links = replace_links(all_links)

    # Save links to the determined file
    save_v2ray_links(updated_links, filename)

    # Determine base64 filename based on the current file
    base64_filename = 'base64' if 'v2tel_links1.txt' in filename else 'base64_1'

    # Encode the entire file content to base64 and save it, overwriting the previous content
    encode_file_to_base64(filename, base64_filename)

if __name__ == "__main__":
    main()

