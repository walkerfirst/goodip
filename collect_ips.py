import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
    'https://ip.164746.xyz'
]

urls_table = [
    'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz'
]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查 ip.txt 文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

count = 0       # 全局计数器，记录第几个IP
written = 0     # 已写入数量

with open('ip.txt', 'w') as file:
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        if url in urls_table:
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('li')

        for element in elements:
            element_text = element.get_text()
            ip_matches = re.findall(ip_pattern, element_text)

            for ip in ip_matches:
                count += 1
                # 从第6个开始，只取偶数，最多8个
                #if count >= 1 and (count % 2 == 0) and written < 8:
                if count >= 1 and written <= 7:
                    file.write(f"{ip}#优选 {written+1} ({ip})\n")
                    written += 1

print('IP地址已保存到 ip.txt 文件中。')
