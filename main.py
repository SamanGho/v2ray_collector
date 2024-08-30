import requests
from bs4 import BeautifulSoup
import os
import time

# Function to extract V2Ray links
def extract_v2ray_links(url,timeout=15,retries=5,retry_delay=8):
    attempt=0
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
        except(requests.exceptions.RequestException , requests.exceptions.Timeout) as e :
            print(f"Attempt {attempt +1} failed {url} :  {e} ")
            attempt+=1 
            time.sleep(retry_delay)
    print("All {retries} attempts to collect failed for {url} ")
    return []
# Function to save V2Ray links to a file, avoiding duplicates
def save_v2ray_links(links , filename="v2tel_link.txt"):
    if links:
        if os.path.exists(filename):
            with open(filename ,'r',encoding='utf-8') as file:
                existing_links=set(file.read().splitlines())
        else :
            existing_links=set()

        new_links=set(links)-existing_links
        with open(filename,'a',encoding='utf-8') as file:
            for link in new_links:
                file.write(link +'\n')


def main():
    telegram_urls = [

        "https://t.me/s/v2ray_configs_pool",
 
        "https://t.me/s/ConfigsHUB2",
        "https://t.me/s/PrivateVPNs",
        "https://t.me/s/VlessConfig", 

        "https://t.me/s/DirectVPN",
               
        "https://t.me/s/FreeV2rays",

        "https://t.me/s/freev2rayssr",
        "https://t.me/s/DailyV2RY",
  
        "https://t.me/s/v2ray_outlineir",
        "https://t.me/s/PrivateVPNs",
    
        "https://t.me/s/vmessq"
        


    ]


    all_links = []
    for url in telegram_urls:
        links = extract_v2ray_links(url)
           # print(f"extracting from {url}   ...  ")
        all_links.extend(links)
           # os.system("cls" if os.name=='nt' else 'clear')
        
    save_v2ray_links(all_links)
        #pathtosave=os.system("cd" if os.name=='nt' else 'pwd')
    #print(f"Extracted and saved {len(all_links)} into v2tel_link.txt  ")
        


if __name__ == "__main__":
    main()
