import re
import sys
import json
import uuid
import requests
import hashlib
import time

from bs4 import BeautifulSoup
import requests

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '*'
APP_SECRET = '*'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def translate(origin):
    data = {'from': 'en', 'to': 'zh-CHS', 'signType': 'v3'}
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(origin) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = origin
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = "您的用户词表ID"

    response = do_request(data)
    if response.status_code == 200:
        res = json.loads(response.content.decode('utf-8'))
        if ('errorCode' in res) and res['errorCode'] == '0':
            return res['translation'][0]
    return 'Error Translation'


def get_html(target):
    req = requests.get(url=target)
    html = req.text
    return BeautifulSoup(html, 'html.parser')


def get_abstract(url):
    tmp = get_html(url)
    if re.search(r'aaai.', url):
        try:
            return tmp.find_all('section', class_='item abstract')[0].text
        except TypeError:
            return 'Error occurred'
    elif re.search(r'doi.org', url):
        try:
            return tmp.find_all('div', class_='abstractSection abstractInFull')[0].contents[1].contents[0]
        except TypeError:
            return 'Error occurred'
    elif re.search(r'openreview.', url):
        try:
            return tmp.contents[1].contents[1].contents[0].contents[3].contents[0].contents[0].contents[0].contents[0].contents[0].contents[3].contents[1].contents[2].contents[0]
        except TypeError:
            return 'Error occurred'
    elif re.search(r'proceedings', url):
        try:
            return tmp.find_all('div', class_='abstract')[0].contents[0]
        except TypeError:
            return 'Error occurred'
    else:
        return 'Unknown type'


def save_file(url, name):
    bf = get_html(url)
    titles = bf.find_all('span', class_='title')
    with open("./" + name + ".txt", "w", encoding='utf-8') as file:
        i = 1
        for title in titles:
            try:
                if re.search(r'Federated', title.string) and title.parent.parent.ul.div.next_sibling.ul.li.a['href']:
                    url = title.parent.parent.ul.div.next_sibling.ul.li.a['href']
                    file.write(str(i) + '. ' + title.string + '\n')
                    file.write(url + '\n\n')
                    abstract = get_abstract(url)
                    file.write(abstract + '\n\n')
                    file.write(translate(abstract) + '\n\n')
                    i += 1
            except TypeError:
                continue
    i -= 1
    print(name + ' done. ' + str(i) + '/' + str(len(titles)))


if __name__ == "__main__":
    # save_file('https://dblp.uni-trier.de/db/conf/aaai/aaai2021.html', 'aaai2021')
    # save_file('https://dblp.uni-trier.de/db/conf/icml/icml2021.html', 'icml2021')
    # save_file('https://dblp.uni-trier.de/db/conf/ccs/ccs2021.html', 'ccs2021')
    # save_file('https://dblp.uni-trier.de/db/conf/iclr/iclr2021.html', 'iclr2021')

    save_file('https://dblp.uni-trier.de/db/conf/aaai/aaai2020.html', 'aaai2020')
    save_file('https://dblp.uni-trier.de/db/conf/icml/icml2020.html', 'icml2020')
    save_file('https://dblp.uni-trier.de/db/conf/ccs/ccs2020.html', 'ccs2020')
    save_file('https://dblp.uni-trier.de/db/conf/iclr/iclr2020.html', 'iclr2020')

    save_file('https://dblp.uni-trier.de/db/conf/aaai/aaai2019.html', 'aaai2019')
    save_file('https://dblp.uni-trier.de/db/conf/icml/icml2019.html', 'icml2019')
    save_file('https://dblp.uni-trier.de/db/conf/ccs/ccs2019.html', 'ccs2019')
    save_file('https://dblp.uni-trier.de/db/conf/iclr/iclr2019.html', 'iclr2019')
