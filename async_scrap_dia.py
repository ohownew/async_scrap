import asyncio
import httpx
import time
import json
import pandas as pd


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
    # "https://www.google.com"
]
# targetURL = f'https://www.igi.org.cn/igi_new.php?r={igi}' # igi请求地址 
index = 0 # urls的索引，标记当前爬到第几个了
df = pd.DataFrame(columns=['text'])


async def check_one_ip(url, i, proxies=None):
    global index
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"
    }
    TIMEOUT = 20
    print(i, "url start scraping...", time.strftime(r"%y-%m-%d %H:%M:%S"))

    try:
        async with httpx.AsyncClient(headers=headers, proxies=proxies, timeout=TIMEOUT) as client:
            response = await client.get(url)
            print(f"response from {url} is : {response.status_code}", time.strftime(r"%y-%m-%d %H:%M:%S"))
            if 200 <= response.status_code < 300:
                df.loc[url] = response.text
            else:
                df.loc[url] = response.status_code
    except  Exception as e:
        print(f"{i} met timeout error", time.strftime(r"%y-%m-%d %H:%M:%S"))
        df.loc[i] = "met timeout error"

    print(i, "url end scraping...", time.strftime(r"%y-%m-%d %H:%M:%S"))

    if index >= len(urls):
        pass
    else:
        task = asyncio.create_task(check_one_ip(urls[index], index, proxies=get_proxy()))
        index += 1
        await task


def get_proxy():
    res_ips = httpx.get(f'https://share.proxy.qg.net/get?key={authKey}&num=1&pool=1')
    res_ips = json.loads(res_ips.content) # 从青果代理获取到的一组ip
    proxyAddr = res_ips['data'][0]['server']
    # 账密模式
    proxyUrl = f"http://{authKey}:{password}@{proxyAddr}" # 青果代理的API
    proxies = {
        "http://": proxyUrl,
        "https://": proxyUrl,
    }
    return proxies


async def main(concurr_num):
    global index
    tasks=[]
    for _ in range(concurr_num):
        task = asyncio.create_task(check_one_ip(urls[index], index, proxies=get_proxy()))
        tasks.append(task)
        index += 1

    await asyncio.wait(tasks)
        

if __name__=="__main__":
    start = time.time()
    asyncio.run(main(3))
    end = time.time()
    print(f"total time: {end-start:.3f}s")
    df.to_pickle('../../test.pkl')