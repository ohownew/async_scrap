"""
n个任务并发的协程爬虫
"""
import asyncio
import time
import requests
import pandas as pd
import json

async def req(url, headers, payload):
    return requests.request("POST", url, headers=headers, json=payload)

async def test(page):
    print(f"Start test({page}) at {time.strftime('%X')}")

    url = "http://zjj.sz.gov.cn/szfdcscjy/esf/publicity/getHouseSourcelibraryList"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
    }
    payload={"district":-1,"pageIndex":page,"pageSize":5,"dateSort":1} # ,"houseStatus":1

    response = asyncio.wait(requests.request("POST", url, headers=headers, json=payload))

    df_fangGP_stock_new = pd.DataFrame(json.loads(response.text)['data']['list'])

    global df_fangGP_stock
    df_fangGP_stock = pd.concat([df_fangGP_stock, df_fangGP_stock_new] , axis=0, ignore_index=True)
    

    print(f"End test({page}) at {time.strftime('%X')}")

    global i
    # 执行完毕上面的协程后，创建一个新协程
    if (i < 10):
        i += 1
        task = asyncio.create_task(test(i))
        await task
        


async def main3(n):
    tasks = []
    # 把任务注册到loop中
    for t in range(n):
        tasks.append(asyncio.create_task(test(t+1)))
    # await任务
    for t in range(n):
        await tasks[t]


if __name__ == '__main__':
    i = 3 # 并发数量，同时也作为游标

    df_fangGP_stock = pd.DataFrame()

    asyncio.run(main3(i))

    df_fangGP_stock.to_clipboard()
