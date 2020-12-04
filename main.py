import os
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
PROXIES = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809"
}
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.116 Safari/537.36",
    "Host": "uclub.ucloud.cn"
}


def login() -> (requests.session, int):
    url = "https://uclub.ucloud.cn/index/user/login.html"
    session = requests.Session()
    f = session.get(url, headers=HEADERS)
    soup = BeautifulSoup(f.text, 'html.parser')
    token = soup.find(attrs={"name": "__token__"})['value']
    data = {
        "__token__": token,
        "account": USERNAME,
        "password": PASSWORD,
        "keeplogin": "1"
    }
    f = session.post(url, headers=HEADERS, data=data)
    f.raise_for_status()
    if f.text.find("登录成功") == -1:
        return None
    return session


def getCredit(session) -> int:
    url = "https://uclub.ucloud.cn/index/user/index.html"
    f = session.get(url, headers=HEADERS)
    soup = BeautifulSoup(f.text, 'html.parser')
    cred = int(soup.find('a', class_='viewscore').text)
    return cred


def signin(session):
    url = "https://uclub.ucloud.cn/index/signin/dosign.html"
    f = session.post(url)
    soup = BeautifulSoup(f.text, 'html.parser')
    print(soup.find('h1').text)


if __name__ == '__main__':
    s = login()
    if not s:
        print("登陆失败，请检查你的登录信息是否准确")
        exit(1)
    else:
        print('登陆成功，您目前的积分为: %d' % getCredit(s))
        signin(s)
        print('签到完成，您目前的积分为: %d' % getCredit(s))
