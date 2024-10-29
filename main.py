import requests
from bs4 import BeautifulSoup
import os
import shutil
from datetime import datetime
import urllib.parse


def get_v2ray_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        divs = soup.find_all('div', class_='tgme_widget_message_text')
        divs2 = soup.find_all('div', class_='tgme_widget_message_text js-message_text before_footer')
        spans = soup.find_all('span', class_='tgme_widget_message_text')
        codes = soup.find_all('code')
        span = soup.find_all('span')
        main = soup.find_all('div')
        
        all_tags = divs + spans + codes + divs2 + span + main

        v2ray_configs = []
        for tag in all_tags:
            text = tag.get_text()
            if text.startswith('vless://') or text.startswith('ss://') or text.startswith('trojan://') or text.startswith('tuic://'):
                v2ray_configs.append(text)

        return v2ray_configs
    else:
        print(f"Failed to fetch URL (Status Code: {response.status_code})")
        return None

def get_region_from_ip(ip):
    api_endpoints = [
        f'https://ipapi.co/{ip}/json/',
        f'https://ipwhois.app/json/{ip}',
        f'http://www.geoplugin.net/json.gp?ip={ip}',
        f'https://api.ipbase.com/v1/json/{ip}'
    ]

    for endpoint in api_endpoints:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                if 'country' in data:
                    return data['country']
        except Exception as e:
            print(f"Error retrieving region from {endpoint}: {e}")
    return None

def save_configs_by_region(configs):
    config_folder = "sub"
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)

    region_dict = {}
    for config in configs:
        ip = config.split('//')[1].split('/')[0]
        region = get_region_from_ip(ip)
        if region:
            if region not in region_dict:
                region_dict[region] = []
            region_dict[region].append(config)
            
    with open(os.path.join(config_folder, 'region_configs.txt'), 'w', encoding='utf-8') as file:
        for region, configs_list in region_dict.items():
            file.write(f"Region: {region}\n")
            for config in configs_list:
                file.write(config + '\n')
            file.write('\n')

if __name__ == "__main__":
    telegram_urls = [
        "https://t.me/s/ConfigV2rayNG",
        "https://t.me/s/beiten",
        "https://t.me/s/DailyV2RY",
        "https://t.me/s/yaney_01",
        "https://t.me/s/v2rayNG_VPNN",
        "https://t.me/s/V2rayNG3",
        "https://t.me/s/VmessProtocol",
        "https://t.me/s/FreeV2rays",
        "https://t.me/s/DigiV2ray",
        "https://t.me/s/frev2rayng"
    ]

    all_v2ray_configs = []
    for url in telegram_urls:
        v2ray_configs = get_v2ray_links(url)
        if v2ray_configs:
            all_v2ray_configs.extend(v2ray_configs)

    if all_v2ray_configs:
        save_configs_by_region(all_v2ray_configs)
        print("Configs saved successfully.")
    else:
        print("No V2Ray configs found.")
