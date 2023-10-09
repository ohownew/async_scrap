import asyncio

async def fun_1():
    for _ in range(5):
        print('协程任务1...')
        await asyncio.sleep(1)


async def fun_2():
    for _ in range(5):
        print('协程任务2...')
        await asyncio.sleep(1)

tasks = [
    fun_1(),
    fun_2()
]

# 3.6以下写法
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks)) 


# 3.7以上写法
asyncio.run(asyncio.wait(tasks))