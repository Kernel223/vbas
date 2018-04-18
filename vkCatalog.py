from urllib.request import Request, build_opener, HTTPCookieProcessor

import sqlite3

from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
from random import randint
from datetime import datetime

def getHtml(url):
    req = Request(url, None, {'User-Agent': 'Mozilla/5.0 (X11; Linux i686;)'})
    cj = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cj))
    response = opener.open(req)
    raw_response = response.read().decode('utf8', errors='ignore')
    response.close()

    return raw_response



def getRandUss(c):
    iNt = str(randint(0, int(c)))
    html = getHtml('https://vk.com/catalog.php?selection={}'.format(iNt))
    soup = BeautifulSoup(html, 'html.parser')
    c = soup.find('div', class_="catalog_wrap clear_fix").find_all('a')[-1].get('href').split('-')[-1]


    TtT = iNt + '-' + str(c)
    html = getHtml('https://vk.com/catalog.php?selection={}'.format(TtT))
    print(iNt,TtT,c)

    soup = BeautifulSoup(html, 'html.parser')
    tt = set()
    t = soup.find('div', class_="catalog_wrap clear_fix").find_all('a')
    print('len t',len(t))
    conn = sqlite3.connect('usrs.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER UNIQUE)''')
    for i, g in enumerate(t):

        h = getHtml("https://vk.com/"+g.get('href'))
        A = BeautifulSoup(h,'html.parser').find('div', class_="catalog_wrap clear_fix").find_all('a')
        for a in A:
            tt.add(a.get('href')[2:])
            # print(a)
            # print(a.get('href'))
            # print(type(a.get('href')))
            # exit()
        print(i)
        # break
    # print(tt)
    print(len(tt))

    conn.commit()
    ti = 0
    for i,t in enumerate(tt):
        c.execute('INSERT INTO users VALUES (?)', [t])

        ti += 1
        if ti - 10 == 0:
            print(i)
            ti = 0

    conn.commit()
    conn.close()
    # Except на 0 tt

    return html

def main(v):
    print(v)
    url = 'http://vk.com/catalog.php'

    html = getHtml(url)

    soup = BeautifulSoup(html,'html.parser')
    c = soup.find('div', class_="catalog_wrap clear_fix").find_all('a')[-1].get('href').split('=')[-1]

    getRandUss(c)
    del c





if __name__ == '__main__':
    now = datetime.now()
    print(now)
    for i in range(0,10):
        main(i)
    end = datetime.now()
    print(end - now)

# open('/home/alex/Desktop/t.html','w').write(raw_response)
# print(len(r))
# print(r)