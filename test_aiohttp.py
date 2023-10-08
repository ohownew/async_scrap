import aiohttp
import asyncio
import json

async def req(i):
    params = {'name': 'germey', 'age': i}
    async with aiohttp.ClientSession() as session:
        async with aiohttp.get('https://httpbin.org/get', params=params) as response:
            res = await response.text()
    
    return json.loads(res)['args']


async def main():
    tasks = [req(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    print(results)


if __name__ == '__main__':

    asyncio.run(main())
    # asyncio.get_event_loop().run_until_complete(main())
