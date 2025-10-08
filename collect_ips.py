import os
import requests
from bs4 import BeautifulSoup
import re

# 最大ip数量
max_ip_count = 8
# 获取新的IP地址
all_ip_matches = []

# 存放ip的文件
ip_file = 'ip.txt'
log_file = 'log.txt'

if os.path.exists(log_file):
    os.remove(log_file)

# table格式
urls_table = ['https://ip.164746.xyz',"https://www.wetest.vip/page/cloudflare/address_v4.html",
    "https://api.uouin.com/cloudflare.html"]
# 目标URL列表
urls = ['https://ip.164746.xyz',"https://www.wetest.vip/page/cloudflare/address_v4.html"]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

for url in urls:
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        if url in urls_table:
            # 对于表格格式的网站，查找表格行
            elements = soup.find_all('tr')
            print(f"{url}: 找到 {len(elements)} 个表格行")
            if "www.wetest.vip" not in url:
                for element in elements:
                    element_text = element.get_text()
                    ip_matches = re.findall(ip_pattern, element_text)
                    all_ip_matches.extend(ip_matches)
                
            else:
                for element in elements:
                    # 查找线路名称列
                    line_name_td = element.find('td', {'data-label': '线路名称'})
                    if line_name_td and '联通' in line_name_td.get_text():
                        # 查找优选地址列
                        ip_td = element.find('td', {'data-label': '优选地址'})
                        if ip_td:
                            ip_text = ip_td.get_text(strip=True)
                            ip_matches = re.findall(ip_pattern, ip_text)
                            if ip_matches:
                                all_ip_matches.extend(ip_matches)
                                print(f"找到联通IP: {ip_matches[0]}")
        else:
            # 对于列表格式的网站
            elements = soup.find_all('li')
            print(f"{url}: 找到 {len(elements)} 个列表项")
            
            for element in elements:
                element_text = element.get_text()
                ip_matches = re.findall(ip_pattern, element_text)
                all_ip_matches.extend(ip_matches)
            
    except Exception as e:
        print(f"处理 {url} 时出错: {e}")
        continue

# 去重并限制数量
all_ip_matches = list(set(all_ip_matches))  # 去重
all_ip_matches = all_ip_matches[:max_ip_count]

print(f"最终获取到 {len(all_ip_matches)} 个唯一IP: {all_ip_matches}")

# 将所有获取的ip保存在 log_file中
with open(log_file, 'w', encoding='utf-8') as _file:
    _file.write('获取到的所有ip为:' + '\n')
    for ip in all_ip_matches:
        _file.write(ip + '\n')

# 读取原有文件内容
original_lines = []
if os.path.exists(ip_file):
    try:
        # 尝试多种编码
        encodings = ['utf-8']
        for encoding in encodings:
            try:
                with open(ip_file, 'r', encoding=encoding) as file:
                    original_lines = file.readlines()
                print(f"成功使用 {encoding} 编码读取文件")
                break
            except UnicodeDecodeError:
                continue
    except Exception as e:
        print(f"读取文件时出错: {e}")
        original_lines = []

# 写入文件，替换IP但保持原有格式
with open(ip_file, 'w', encoding='utf-8') as file:
    # 如果原行数大于或等于获取的ip数量
    if len(all_ip_matches) <= len(original_lines):
        for i, line in enumerate(original_lines):
            if i < len(all_ip_matches):
                # 替换该行的IP地址
                new_ip = all_ip_matches[i]
                # 假设格式为 "IP#优选 序号 (IP)"
                new_line = f"{new_ip}#优选 {i+1} ({new_ip})\n"
                file.write(new_line)
            else:
                # 如果新IP数量少于原文件行数，保留原行
                if i < max_ip_count:
                    file.write(line)
    # 原文件行数小于获取的ip数量
    else:
        for j, ip in enumerate(all_ip_matches):
            _line  = f"{ip}#优选 {j+1} ({ip})\n"
            file.write(_line)

print(f'IP地址已更新到 ip.txt 文件中。共获取 {len(all_ip_matches)} 个IP。')