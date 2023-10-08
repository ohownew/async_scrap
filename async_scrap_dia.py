import asyncio
import httpx
import time
import json
from parsel import Selector

# 青果账密
authKey = "KZ4VXNJP"
password = "4BE6158FBCC4"

# 测试时将测试网址替换
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
    "https://www.google.com"
]


async def check_one_ip(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"
    }
    TIMEOUT = 100
    result = ()
    res_ips = httpx.get(f'https://share.proxy.qg.net/get?key={authKey}&num=1&pool=1')
    res_ips = json.loads(res_ips.content) # 从青果代理获取到的一组ip
    proxyAddr = res_ips['data'][0]['server']
    # targetURL = f'https://www.igi.org.cn/igi_new.php?r={igi}' # igi请求地址 
    # 账密模式
    proxyUrl = f"http://{authKey}:{password}@{proxyAddr}" # 青果代理的API
    proxies = {
        "http://": proxyUrl,
        "https://": proxyUrl,
    }

    try:
        async with httpx.AsyncClient(headers=headers, proxies=proxies, timeout=TIMEOUT) as client:
            response = await client.get(url)
            print(f"response from {url} is : {response.status_code}")
            if 200 <= response.status_code < 300:
                print(f"length of response body is {len(response.text)}")
            result = (url, response.status_code)
    except  Exception as e:
        print(f"{url} met timeout error")
        return (url, 999)
    return result 

def task_callback(context):
    # print response.status_code 
    url, code = context.result()
    print(f"It is callback,  got status_code: {code} of {url}")

async def main():
    tasks=[]
    for url in urls:
        task = asyncio.create_task(check_one_ip(url))
        # task.add_done_callback(task_callback)
        tasks.append(task)
    await asyncio.gather(*tasks) 
        

if __name__=="__main__":
    t1 = time.time()
    asyncio.run(main())
    t2 = time.time()
    print(f"total time: {t2-t1:.3f}s")