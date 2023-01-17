import requests
import os
import inspect
import json
from bs4 import BeautifulSoup

f = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0] + "/cpu_additional_info.json"


class MatchPart(str):
    def __eq__(self, other):
        return self.__contains__(other)


def search(term: str):
    get = requests.get(f"https://www.techpowerup.com/cpu-specs/?ajaxsrch={term}")
    soup = BeautifulSoup(get.text, "html.parser")
    results = soup.find_all('a', href=True)
    names = [i.contents[0] for i in results]
    links = [i['href'] for i in results]
    ret = list(zip(names, links))
    for idx, name in enumerate(names):
        if name.lower() == term.lower():
            return list(ret[idx])
        if name.lower().startswith(term.lower()) or name.lower().endswith(term.lower()):
            return list(ret[idx])
    return tuple(ret[0])


def process(tags: list):
    ret = []
    for tag in tags:
        try:
            ret.append(str(tag.contents[0].get_text()).strip())
        except IndexError:
            ret.append('(unknown)')
    return ret


def run(term: str):
    item = search(term)
    info = json.load(open(f, "r"))
    info_match = [d['match'] for d in info]
    name = item[0]
    link = item[1]
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 Safari/537.36"
    }
    r = requests.get(f"https://www.techpowerup.com{link}",
                     headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        note = soup.select('td.p')[0].contents[0]
    except IndexError:
        note = None
    x = soup.find_all('td')
    x1 = process(x)
    y = soup.find_all('th')
    y1 = process(y)
    out = dict(zip(y1, x1[:-1]))
    # General info
    ret = {
        "Name": name,
        "Release date": out['Release Date:'],
        "Codename": out['Codename:'],
        "Vertical Segment": out['Market:'],
        "Fabrication process": out['Process Size:']
    }
    # Cores and threads
    ret |= {
        "Cores": out['# of Cores:'],
        "Threads": out['# of Threads:'],
        "Is unlocked": out['Multiplier Unlocked:']
    }
    if (ret['Cores'] != ret['Threads']) and (int(ret['Cores']) != int(ret['Threads']) // 2):
        # Hybrid architecture (SOME Intel 12th gen or later)
        ret |= {
            "Cores": f'{int(ret["Threads"]) - int(ret["Cores"])} P-cores, {2 * int(ret["Cores"]) - int(ret["Threads"])} E-cores ({ret["Cores"]} total)',
            "P-core base frequency": out['Frequency:'],
            "E-core base frequency": out['E-Core Frequency:'],
            "P-core turbo frequency": out['Turbo Clock:'],
            "E-core turbo frequency": out['E-Core Turbo Clock:'],
            "Base power": out['TDP:'],
            "Turbo power": f'PL1: {out["PL1:"]}, PL2: {out["PL2:"]}, boost window: {out["PL2 Tau Limit:"]}',
            "P-core L1 cache": out['Cache L1:'],
            "P-core L2 cache": out['Cache L2:']
        }
        if 'E-Core L1:' in out:
            ret |= {
                "E-core L1 cache": out['E-Core L1:'],
                "E-core L2 cache": out['E-Core L2:']
            }
    else:
        ret |= {
            "Base frequency": out['Frequency:'],
            "Turbo frequency": out['Turbo Clock:'],
            "TDP": out['TDP:']
        }
        if 'PPT:' in out:
            ret |= {"APU PPT": out['PPT:']}
        ret |= {
            "L1 cache": out['Cache L1:'],
            "L2 cache": out['Cache L2:']
        }
    if 'Cache L3:' in out:
        ret |= {
            "L3 cache": out['Cache L3:']
        }
    if note is not None:
        ret |= {"\n*Note": f"{note}*"}

    return [r.status_code, ret]
