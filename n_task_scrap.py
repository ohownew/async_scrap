"""
n个任务并发的协程爬虫
"""
import asyncio
import time

async def test(number):
    print(f"Start test({number}) at {time.strftime('%X')}")
    await asyncio.sleep(number)
    print(f"End test({number}) at {time.strftime('%X')}")
    global i
    results[number-1] = number
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
    results = [0] * 10

    print(results)
    asyncio.run(main3(i))
    print(results)