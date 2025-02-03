
import re
import requests
from bs4 import BeautifulSoup
import os
import time
import sys
import base64
def read_counter():
    '''Read the counter val from a file'''
    try:
        with open('run_counter.txt','r') as f:
            return int(f.read().strip())
    except (FileNotFoundError , ValueError):
        return 1 
def increment_counter(current_count):
    '''Increment the counter & handle trunc'''
    current_count+=1
    with open('run_counter.txt','w') as f:
        f.write(str(current_count))
    if current_count>12:
        truncate_files()

        current_count=1
        with open('run_counter.txt','w') as f:
            f.write('1')
    return current_count

def truncate_files():
    '''Truncate files starting from first  meaningful link'''
    files_to_truncate=['v2tel_links1.txt','v2tel_links2.txt']

    link_pattern=re.compile(r'(vless://|vmess://|trojan://|ss://)')

    for filename in files_to_truncate:
        try:
            with open(filename , 'r', encoding='utf-8') as f:
                content=f.read()

            matcham= link_pattern.search(content)
            if matcham:
                truncated_content=content[matcham.start():]
            else:
                midpoint = len(content) //2
                truncated_content=content[midpoint:]
            

            with open(filename , 'w' , encoding='utf-8') as f:
                f.write(truncated_content)

        except FileNotFoundError:
            print(f"File {filename} not found skipping ")
        except Exception as e:
            print(f'Erorr truncating {filename} : {e})')
        
                  
def gather_last_150_links():
    '''
    Gather the last 150 links from v2tel_links1 & 2.txt  save them 
    '''           
    input_files=['v2tel_links1.txt','v2tel_links2.txt']
    output_file='last_150.txt'
    all_links=[]

    for filename in input_files:
        try:
            with open(filename,'r',encoding='utf-8') as f:
                file_links=[link.strip() for link in f.readlines() if link.strip() ]
            
                all_links.extend(file_links)
        except FileNotFoundError:
            print(f"File {filename} not found skipping")
        except Exception as e :
            print(f" Error reading {filename} {e}")
            continue
    unique_links=[]
    seen=set()
    for link in all_links:
        if link not in seen:
            unique_links.append(link)
            seen.add(link)
    
    last_links = unique_links[-150:]

    try:

        with open(output_file,'w',encoding='utf-8') as f:
            for link in last_links:
                f.write(link+'\n')
        print(f'Saved {len(last_links)} unique links to {output_file}')
    except Exception as e:
        print(f" Error writing to {output_file}:{e}")


def extract_v2ray_links(url, timeout=15, retries=5, retry_delay=8):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                v2ray_links = []

                # Find all divs with the specific class and extract the links
                for div in soup.find_all('div', class_=lambda x: x and 'tgme_widget_message_text' in x):
                    pre_tag = div.find('pre')
                    code_tag = div.find('code')
                    
                    # Check pre tag
                    if pre_tag and pre_tag.text.strip().startswith(('vless://','vmess://','trojan://','ss://')):
                        v2ray_links.append(pre_tag.text.strip())
                    
                    # Check code tag
                    if code_tag and code_tag.text.strip().startswith(('vless://', 'vmess://', 'trojan://', 'ss://')):
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
    if not os.path.exists('run_counter.txt'):
        with open('run_counter.txt', 'w') as f:
            f.write('1')
    
    current_count=read_counter()
    current_count=increment_counter(current_count)

    if len(sys.argv) < 2:
        print("Error: Filename argument is missing.")
        sys.exit(1)

    filename = sys.argv[1]


    telegram_urls = [
        "https://t.me/s/V2razy",
        'https://t.me/s/v2ray_configs_pool',
        'https://t.me/s/ConfigsHUB2',
        "https://t.me/s/ConfigsHUB",
        "https://t.me/s/PrivateVPNs",
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

    # Replace links before saving
    updated_links = replace_links(all_links)

    # Save links to the determined file
    save_v2ray_links(updated_links, filename)
    try:
        gather_last_150_links()
    except Exception as e:
        print(f"Error in gather_last_150_links: {e}")
    
    base64_filename = 'base64' if 'v2tel_links1.txt' in filename else 'base64_1'

    encode_file_to_base64(filename, base64_filename)

if __name__ == "__main__":
    main()

