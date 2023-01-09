import requests

from bs4 import BeautifulSoup


def run():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 Safari/537.36"
    }
    r = requests.get(f"https://www.techpowerup.com/cpu-specs/core-i9-12900ks.c2598",
                     headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    x = soup.find_all('td')
    x1 = process(x)
    y = soup.find_all('th')
    y1 = process(y)
    out = [b + ' ' + a for b, a in zip(y1, x1[:-2])]
    return out


def process(tags: list):
    ret = []
    for tag in tags:
        try:
            ret.append(str(tag.contents[0].get_text()).strip())
        except IndexError:
            ret.append('(unknown)')
    return ret
