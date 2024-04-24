import requests
import json
import time

# 青果账密
authKey = "xxxxxxx"
password = "xxxxxxxx"


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
        "http": proxyUrl,
        "https": proxyUrl,
    }
    return proxies

start = time.time()
for url in urls:
    proxies=get_proxy()
    res = requests.get(url, proxies=proxies)
    print(proxies['http'], res.status_code, url, time.strftime(r"%y-%m-%d %H:%M:%S"))
end = time.time()
print("总耗时：", end-start)
