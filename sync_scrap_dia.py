import requests
import json

# 青果账密
authKey = "KZ4VXNJP"
password = "4BE6158FBCC4"


urls = [
    "https://www.baidu.com",
    "https://www.baidu.com",
    "https://www.baidu.com",
    "https://www.baidu.com",
    "https://www.baidu.com",
    "https://www.baidu.com",
    "https://www.baidu.com",
    "https://www.baidu.com",
    "https://www.baidu.com",
    "https://www.baidu.com",
    "https://www.baidu.com",
    # "https://www.google.com"
]

def get_proxy():
    res_ips = requests.get(f'https://share.proxy.qg.net/get?key={authKey}&num=1&pool=1')
    res_ips = json.loads(res_ips.content) # 从青果代理获取到的一组ip
    proxyAddr = res_ips['data'][0]['server']
    # 账密模式
    proxyUrl = f"http://{authKey}:{password}@{proxyAddr}" # 青果代理的API
    proxies = {
        "http://": proxyUrl,
        "https://": proxyUrl,
    }
    return proxies

for url in urls:
    requests