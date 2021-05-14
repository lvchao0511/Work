# Requests库的爬取性能分析
import requests
import time

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.61 Safari/537.36 Edg/90.0.818.36'
}


def get_html_text(url):
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '异常'


time_0 = time.time()
for i in range(100):
    r = requests.get('http://www.bing.com', headers=header)
    print('{} {:.2f}s'.format(i+1, time.time()-time_0))
