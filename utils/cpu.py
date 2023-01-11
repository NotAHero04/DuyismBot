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
    out = dict(zip(y1, x1[:-2]))
    # General info
    ret = {
        "Release date": out['Release Date:'],
        "Codename": out['Codename:'],
        "Vertical Segment": out['Market:'],
        "Fabrication process": out['Process Size:']
    }
    # Cores and threads
    ret |= {
        "Cores": int(out['# of Cores:']),
        "Threads": int(out['# of Threads:'])
    }
    if ret['Cores'] != ret['Threads'] and ret['Cores'] != ret['Threads'] // 2:
    # Hybrid architecture (Intel 12th gen or later)
        ret |= {
            "Cores": {
                "P-cores": ret['Threads'] - ret['Cores'],
                "E-cores": 2 * ret['Cores'] - ret['Threads']
            },
            "Base frequency": {
                "P-cores": out['Frequency:'],
                "E-cores": out['E-Core Frequency:']
            },
            "Turbo frequency": {
                "P-cores": out['Turbo Clock:'],
                "E-cores": out['E-Core Turbo Clock:']
            },
            "Cache": {
                "P-cores": {
                    "L1": out['Cache L1:'],
                    "L2": out['Cache L2:']
                },
                "E-cores": {
                    "L1": out['E-Core L1:'],
                    "L2": out['E-Core L2:']
                }
            }
        }
    else:
        ret |= {
            "Base frequency": out['Frequency:'],
            "Turbo frequency": out['Turbo Clock:'],
            "Cache": {
                "L1": out['Cache L1:'],
                "L2": out['Cache L2:']
            },
        }
    ret |= {
        "L3 cache": out['Cache L3:']
    }
    return ret


def process(tags: list):
    ret = []
    for tag in tags:
        try:
            ret.append(str(tag.contents[0].get_text()).strip())
        except IndexError:
            ret.append('(unknown)')
    return ret

# print(run())
