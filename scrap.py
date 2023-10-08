import asyncio
import time
import datetime

async def say_after(delay, what):
    print(f"started at {time.strftime('%X')}", what)
    await asyncio.sleep(delay)
    print(f"finished at {time.strftime('%X')}", what)

async def main():
    task1 = asyncio.create_task( # 注册到loop中
        say_after(1, 'hello'))

    task2 = asyncio.create_task( # 注册到loop中
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


async def display_date():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f


async def test(number):
    print(f"Start test({number}) at {time.strftime('%X')}")
    await asyncio.sleep(number/10)
    print(f"End test({number}) at {time.strftime('%X')}")
    global i
    results[number-1] = number
    # 执行完毕上面的协程后，创建一个新协程
    if (i < 100):
        i += 1
        task = asyncio.create_task(test(i))

        await task
    


async def main2():
    # Schedule three calls *concurrently*:
    cors = []
    for i in range(2, 10):
        cors.append(test(i))

    L = await asyncio.gather(
        *cors
    )
    print(L)


async def main3():
    task1 = asyncio.create_task(test(1))
    task2 = asyncio.create_task(test(2))
    task3 = asyncio.create_task(test(3))

    await task1
    await task2
    await task3

if __name__ == '__main__':
    i = 3
    results = [0] * 100

    print(results)
    # asyncio.run(main())
    # asyncio.run(display_date())


    # Schedule three calls *concurrently*:
    # asyncio.run(main2())
    asyncio.run(main3())
    print(results)