from aip import AipOcr
import re
import json
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

APP_ID = '11406750'
API_KEY = '7S9GOcUDPWuVxBDNXhkeaC3u'
SECRET_KEY = 'BcZYCuXB8tqueUmEu3hN6EayxcFbz18a'
name = '686339'
pwd = 'hj03080127',


client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def getnum(img):
    # 图像识别验证码
    image = img
    res = client.basicGeneral(image, options={'language_type': 'ENG'})
    nums = res['words_result'][0]['words']
    nums = nums.replace(' ', '')
    newnums = nums.replace('.', '')
    print(newnums)
    return newnums


def login(name, passw):
    # 获取验证码
    req = s.get('https://cas.baogang.info/cas/getCaptchaImage?d=1517367419141',
                headers=heads, verify=False)
    code = getnum(req.content)
    # 验证码图像存入文件code.jpg
    with open(r'D:\code.jpg', 'wb') as fn:
        fn.write(req.content)
    print(code)
    user = {
        'username': name,
        'password': passw,
        'useCert': 'false',
        '_captcha_parameter': code,
        'lt': '',
        'execution': 'e1s1',
        '_eventId': 'submit',
    }
    time.sleep(2)
    tt = s.post('https://cas.baogang.info/cas/login?service=http%3A%2F%2Fbes.baosteel.info%3A8080%2Fdominosso%2Fcas_callback%3ForiginalTargetUri%3D%252Findex.jsp%26syscode%3Dbes&baosight=a&baostell=b&baozi=c', headers=heads, data=user)
    tt1 = s.post('https://cas.baogang.info/cas/login?loginType=mixLogin&cssName=bsw2',
                 headers=heads, data=user)
    return tt, tt1


s = requests.session()
# requests.session()维持会话，可以在跨请求时保存某些参数
heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

n = 0
while n < 50:
    try:
        req = login(name, pwd)
        tex = req[1].text.find('<title>Insert title here</title>')
        if tex >= 0:
            print('login')
            n = 51
        else:
            n = 0
    except:
        n = 0
        print('erro')


tt2 = s.request('GET', req[0].history[0].headers['Location'], headers=heads)
tt3 = s.request('GET', 'http://bes.baosteel.info:8080/dominosso/index.jsp;jsessionid=' +
                requests.utils.dict_from_cookiejar(s.cookies)['JSESSIONID'], headers=heads)
# tt2和tt3让requests.session里保存登录信息的cookies
tt4 = s.request(
    'GET', 'http://bes03.baosteel.info/BeSDataBase/SciResearch.nsf/vwTasks_ByStatus?OpenView&Start=1&Count=15&Expand=2', headers=heads)
# tt4内容为任务中心（按状态），通过网页分析network-XHR分析得到

soup0 = BeautifulSoup(tt4.text, 'html.parser')

# table = soup0.find_all(href=re.compile("/BeSDataBase/SciResearch.nsf/"))
# for i in range(len(table)):
#     if len(table[i].find_all(alt=re.compile('Hide details for 季报表_部门联络员审核'))) > 0:
#         start = i
#     if len(re.findall(re.compile("Expand=3#3", re.S), table[i]['href'])) > 0:
#         end = i

# data0 = table[start+1:end]

data0 = soup0.find_all(href=re.compile(
    "^/BeSDataBase/SciResearch.nsf/.*?OpenDocument$"))
# 以/BeSDataBase/SciResearch.nsf/开头（^），以?OpenDocument结尾($)，中间任意（.*）

datas = pd.read_excel(r'D:\科研\科研季报.xlsx')
for i in data0:
    # 实现季报附件的抓取
    url = 'http://bes03.baosteel.info'+i.get('href')
    tt5 = s.request('GET', url, headers=heads)
    # 进入科研项目进展情况季报表
    filetext = BeautifulSoup(tt5.text, 'html.parser').find_all(id="Atts6b_1")
    fileurl = 'http://bes03.baosteel.info' + \
        filetext[0].find_all('a')[0].get('href')
    filename = filetext[0].find_all('a')[0].text
    with open(r'D:\科研\季报\\' + filename, 'wb') as fn:
        fn.write(s.request('GET', fileurl, headers=heads).content)

    datas = datas.append({'名称': filename, '处理建议（Y/N)': '', '备注': '', 'url': fileurl, 'uurl': url,
                          'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}, ignore_index=True)
datas.to_excel(r'D:\科研\科研季报.xlsx', index=False)
