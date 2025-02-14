import re
import requests
from bs4 import BeautifulSoup
import os
import time
import sys
import base64

# Function to read the counter value from a file
def read_counter():
    '''Read the counter value from a file'''
    try:
        with open('run_counter.txt', 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 1

# Function to increment the counter and truncate files if necessary
def increment_counter(current_count):
    '''Increment the counter & handle truncation'''
    current_count += 1
    with open('run_counter.txt', 'w') as f:
        f.write(str(current_count))
    if current_count > 12:
        truncate_files()
        current_count = 1
        with open('run_counter.txt', 'w') as f:
            f.write('1')
    return current_count

# Function to truncate files starting from the first meaningful link
def truncate_files():
    '''Truncate files starting from the first meaningful link'''
    files_to_truncate = ['v2tel_links1.txt', 'v2tel_links2.txt']
    link_pattern = re.compile(r'(vless://|vmess://|trojan://|ss://)')
    for filename in files_to_truncate:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            match = link_pattern.search(content)
            if match:
                truncated_content = content[match.start():]
            else:
                midpoint = len(content) // 2
                truncated_content = content[midpoint:]
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(truncated_content)
        except FileNotFoundError:
            print(f"File {filename} not found, skipping.")
        except Exception as e:
            print(f"Error truncating {filename}: {e}")

# Function to gather the last 150 unique links
def gather_last_150_links():
    '''
    Gather the last 150 unique links from v2tel_links1.txt and v2tel_links2.txt
    and save them to last_150.txt
    '''
    input_files = ['v2tel_links1.txt', 'v2tel_links2.txt']
    output_file = 'last_150.txt'
    all_links = []
    for filename in input_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                file_links = [link.strip() for link in f.readlines() if link.strip()]
                all_links.extend(file_links)
        except FileNotFoundError:
            print(f"File {filename} not found, skipping.")
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    unique_links = list(dict.fromkeys(all_links))  # Preserve order and remove duplicates
    last_links = unique_links[-150:]  # Get the last 150 links
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(last_links))
        print(f"Saved {len(last_links)} unique links to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

# Function to extract V2Ray links from Telegram URLs
def extract_v2ray_links(url, timeout=15, retries=5, retry_delay=8):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                v2ray_links = []
                for div in soup.find_all('div', class_=lambda x: x and 'tgme_widget_message_text' in x):
                    for tag in ['pre', 'code']:
                        element = div.find(tag)
                        if element and element.text.strip().startswith(('vless://', 'vmess://', 'trojan://', 'ss://')):
                            v2ray_links.append(element.text.strip())
                return v2ray_links
            else:
                print(f"Failed to fetch URL: {url}, status code = {response.status_code}")
                return []
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            attempt += 1
            time.sleep(retry_delay)
    print(f"All {retries} attempts to collect failed for {url}")
    return []

# Function to replace specific text in links
def replace_links(links, replacements=None):
    if replacements is None:
        replacements = {}
    updated_links = []
    for link in links:
        for old, new in replacements.items():
            link = link.replace(old, new)
        updated_links.append(link)
    return updated_links

# Function to save V2Ray links to a file, avoiding duplicates
def save_v2ray_links(links, filename):
    existing_links = set()
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_links = set(file.read().splitlines())
    new_links = set(links) - existing_links
    with open(filename, 'a', encoding='utf-8') as file:
        file.write('\n'.join(new_links) + '\n')

# Function to encode a file's content to Base64
def encode_file_to_base64(input_filename, output_filename):
    try:
        with open(input_filename, 'rb') as file:
            content = file.read()
        encoded_content = base64.b64encode(content).decode('utf-8')
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(encoded_content)
        print(f"Encoded {input_filename} to {output_filename}")
    except Exception as e:
        print(f"Error encoding {input_filename}: {e}")

# Main function
def main():
    if not os.path.exists('run_counter.txt'):
        with open('run_counter.txt', 'w') as f:
            f.write('1')

    current_count = read_counter()
    current_count = increment_counter(current_count)

    if len(sys.argv) < 2:
        print("Error: Filename argument is missing.")
        sys.exit(1)
    filename = sys.argv[1]

    telegram_urls = [
        "https://t.me/s/moftconfig",
        "https://t.me/s/ConfigsHUB2",
        "https://t.me/s/VlessConfig",
        "https://t.me/s/DirectVPN",
        "https://t.me/s/FreeV2rays",
        "https://t.me/s/freev2rayssr",
        "https://t.me/s/IP_CF_Config",
        "https://t.me/s/ArV2ray",
        "https://t.me/s/v2ray_outlineir",
        "https://t.me/s/nufilter"
    ]

    all_links = []
    for url in telegram_urls:
        links = extract_v2ray_links(url)
        all_links.extend(links)

    updated_links = replace_links(all_links)
    save_v2ray_links(updated_links, filename)

    try:
        gather_last_150_links()
        encode_file_to_base64('last_150.txt', 'base64_150.txt')  # Encode last_150.txt to Base64
    except Exception as e:
        print(f"Error in gather_last_150_links or encoding: {e}")

if __name__ == "__main__":
    main()
