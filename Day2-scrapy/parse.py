from urllib import parse

url_a = 'http://cn.bing.com/search'
d = {'q': '中文'}

u = parse.urlencode(d)
url = '{}?{}'.format(url_a, u)

print(url)
print('~'*4)
print(parse.unquote(url))
