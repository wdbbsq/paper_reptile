import re

from bs4 import BeautifulSoup
import requests


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


def write_file(url, name):
    bf = get_html(url)
    titles = bf.find_all('span', class_='title')

    with open("./" + name + ".txt", "w", encoding='utf-8') as file:
        i = 1
        for title in titles:
            try:
                if re.search(r'Federated', title.string) and title.parent.parent.ul.div.next_sibling.ul.li.a['href']:
                    url = title.parent.parent.ul.div.next_sibling.ul.li.a['href']
                    file.write(str(i) + '. ' + title.string + '\n')
                    file.write(url + '\n')
                    file.write(get_abstract(url) + '\n\n')
                    i += 1
            except TypeError:
                continue


if __name__ == "__main__":
    # write_file('https://dblp.uni-trier.de/db/conf/aaai/aaai2021.html', 'aaai2021')
    # write_file('https://dblp.uni-trier.de/db/conf/icml/icml2021.html', 'icml2021')
    write_file('https://dblp.uni-trier.de/db/conf/ccs/ccs2021.html', 'ccs2021')
    # write_file('https://dblp.uni-trier.de/db/conf/iclr/iclr2021.html', 'iclr2021')
