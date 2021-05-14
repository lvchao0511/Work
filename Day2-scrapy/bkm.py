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
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
def getnum(img):
    image =img
    res = client.basicGeneral(image,options = {'language_type':'ENG'})
    nums = res['words_result'][0]['words']
    nums = nums.replace(' ','')
    newnums = nums.replace('.','')
    print(newnums)
    return newnums

def login(name,passw):
    req = s.get('https://cas.baogang.info/cas/getCaptchaImage?d=1517367419141',headers=heads,verify=False)
    code = getnum(req.content)
    with open(r'E:\code.jpg', 'wb') as fn:
        fn.write(req.content)
    print(code)
    user = {
    'username':name,
    'password':passw,
    'useCert':'false',
    '_captcha_parameter':code,
    'lt':'',
    'execution':'e1s1',
    '_eventId':'submit',
    }
    time.sleep(2)
    s.post('https://cas.baogang.info/cas/login?loginType=mixLogin&cssName=bsw2',headers=heads,data=user)

    return s.post('https://cas.baogang.info/cas/login?loginType=mixLogin&cssName=bsw2',headers=heads,data=user)

from threading import Timer
names={
    '686287':'lwj686287'


}

def delayed(seconds):
    def decorator(f):
        def wrapper(*args, **kargs):
            t = Timer(seconds, f, args, kargs)
            t.start()
        return wrapper
    return decorator



s = requests.session()
heads = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
passw=names['686287']

print(passw)
n=0
while n==0:
    try:
        req=login('686287',passw)
        n = req.text.find('<title>Insert title here</title>')
        print('login')

    except:
        n=0
        print('erro')
da0 = {
    'i-0-memberId': '686287'
}
ht0 = s.request('POST','http://bkm.baogang.info:9080/BP/PL/BPPLPersonFncMode.jsp',headers=heads,data=da0)
ht0 = s.request('POST','http://bkm.baogang.info:9080/BP/PL/BPPLPersonFncMode.jsp',headers=heads,data=da0)
soup0=BeautifulSoup(ht0.text,'html.parser')
list_id0 = soup0.find_all('a',class_="app")
n = list_id0[2].font.string

da = {
    'i-0-startTime': '',
'i-0-endTime': '',
'i-0-submitUserName':  '',
'i-0-submitUser': '',
'i-0-orgName': '',
'i-0-orgCode': '',
'r-offset': '0',
'r-limit': n,
'taskType': 'taskType',
'r-orderBy': 'ni.create_time ASC',
'r-count': n,
'_Pagination_jumppage':''
}
ht = s.request('POST','http://bkm.baogang.info:9080/DispatchAction.do?efFormEname=BPPATodoList&serviceName=BPPAHome&methodName=queryTask',headers=heads,data=da)

soup=BeautifulSoup(ht.text,'html.parser')
list_tr = soup.find_all('table')
data = []
for i in list_tr[1].find_all('tr')[1:]:
    data.append([i.find_all('td')[0].string,i.find_all('td')[3].string,i.find_all('td')[4].string])
dataframe = pd.DataFrame(data)
dataframe.columns=['名称','姓名','时间']
dataframe.to_csv(r'C:\Users\zzy\Desktop\临时\bkm.csv', encoding='utf_8_sig', index=False, header=True)
     