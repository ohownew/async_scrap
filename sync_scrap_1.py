import requests
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


def check_one_ip(url):
    headers = {
        "user-ageng": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"
    }
    TIMEOUT = 3
    result = ()
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        print(f"response from {url} is : {response.status_code}")
        if 200 <= response.status_code < 300:
            print(f"length of response body is {len(response.text)}")
        result = (url, response.status_code)
    except Exception as e:
        print(f"{url} met timeout error")
        return (url, 999)
    return result


def main():
    results = []
    for url in urls:
        result = check_one_ip(url)
        results.append(result)


if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print(f"total time: {t2-t1:.3f}s")