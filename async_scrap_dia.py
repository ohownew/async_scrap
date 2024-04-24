import asyncio
import httpx
import time
import json
import pandas as pd
import os
from parsel import Selector

# 青果账密
authKey = "xxxxxxxx"
password = "xxxxxxxxx"


root_path = os.path.dirname(__file__)
df_igi = pd.read_excel(root_path + "/data/igis.xlsx")
url_prefix = 'https://www.igi.org.cn/igi_new.php?r='
# 测试时将测试网址替换
urls = [url_prefix + str(igi) for igi in df_igi.iloc[:20, 0]]

index = 0 # urls的索引，标记当前爬到第几个了
igi_params = []
CONCURR_NUM = 4


class Proxy:
    def __init__(self) -> None:
        self.proxy = None
        self.timestamp = None

    def get_proxy(self):
        # 如果时间戳为空、或者距离上次超过15s、或者协程次数达到了并发数的整数倍，则修改时间戳和代理
        if (self.timestamp is None) or (time.time() - self.timestamp > 15) or (index % CONCURR_NUM == 0):
            res_ips = httpx.get(f'https://share.proxy.qg.net/get?key={authKey}&num=1&pool=1')
            res_ips = json.loads(res_ips.content) # 从青果代理获取到的一组ip
            proxyAddr = res_ips['data'][0]['server']
            # 账密模式
            proxyUrl = f"http://{authKey}:{password}@{proxyAddr}" # 青果代理的API
            proxies = {
                "http://": proxyUrl,
                "https://": proxyUrl,
            }
            self.proxy = proxies
            self.timestamp = time.time()
        return self.proxy
    

def parse_html(html):
    selector = Selector(text=html) # 解析网页
    # 获取钻石参数存到字典里
    diamond_params = dict()
    for tr in selector.css('.table-360-report').xpath('./tr'):
        col_name = tr.xpath('./td/text()').get()
        col_val = tr.xpath('./td/b/text()').get()
        diamond_params[col_name] = col_val
    igi_params.append(diamond_params)


async def check_one_ip(url, i, proxies=None):
    global index
    global proxy
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"
    }
    TIMEOUT = 10

    print(i, "url start scraping...", time.strftime(r"%y-%m-%d %H:%M:%S"))

    try:
        async with httpx.AsyncClient(proxies=proxies) as client:
            response = await client.get(url, headers=headers, timeout=TIMEOUT)
            print(f"response from {url} is : {response.status_code}", time.strftime(r"%y-%m-%d %H:%M:%S"))
            if 200 <= response.status_code < 300:
                html = json.loads(response.text)[0]
                parse_html(html)
            else:
                igi_params.append({'url':url, 'reason':str(response.status_code)})
    except httpx.HTTPError as exc:
        print(time.strftime(r"%y-%m-%d %H:%M:%S"), f"HTTP Exception for {exc.request.url} - {exc}")
        igi_params.append({'url':url, 'reason':exc})

    print(i, "url end scraping...", time.strftime(r"%y-%m-%d %H:%M:%S"))

    if index >= len(urls):
        pass
    else:
        task = asyncio.create_task(check_one_ip(urls[index], index, proxies=proxy.get_proxy()))
        index += 1
        await task


async def main(concurr_num):
    global index
    global proxy
    tasks=[]
    for _ in range(concurr_num):
        task = asyncio.create_task(check_one_ip(urls[index], index, proxies=proxy.get_proxy()))
        tasks.append(task)
        index += 1

    await asyncio.wait(tasks)
        

if __name__=="__main__":

    proxy = Proxy() # 初始化代理

    start = time.time()
    asyncio.run(main(CONCURR_NUM))
    end = time.time()

    print(f"total time: {end-start:.3f}s")
    pd.DataFrame(igi_params).to_pickle(root_path+'test.pkl')

