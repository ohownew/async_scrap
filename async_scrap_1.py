import asyncio
import httpx
import time

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
    TIMEOUT = 3
    result = ()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers,timeout=TIMEOUT)
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
        task.add_done_callback(task_callback)
        tasks.append(task)
    await asyncio.gather(*tasks) 
        

if __name__=="__main__":
    t1 = time.time()
    asyncio.run(main())
    t2 = time.time()
    print(f"total time: {t2-t1:.3f}s")