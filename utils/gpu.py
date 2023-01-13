import requests

from bs4 import BeautifulSoup


def search(term: str):
    get = requests.get(f"https://www.techpowerup.com/cpu-specs/?ajaxsrch={term}")
    soup = BeautifulSoup(get.text, "html.parser")
    results = soup.find_all('a', href=True)
    names = [i.contents[0] for i in results]
    links = [i['href'] for i in results]
    return list(zip(names, links))


def process(tags: list):
    ret = []
    for tag in tags:
        try:
            ret.append(str(tag.contents[0].get_text()).strip())
        except IndexError:
            ret.append('(unknown)')
    return ret


def get_info(item: tuple[str, str]):
    name = item[0]
    link = item[1]
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 Safari/537.36"
    }
    r = requests.get(f"https://www.techpowerup.com{link}",
                     headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
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
        "Threads": out['# of Threads:']
    }
    if (ret['Cores'] != ret['Threads']) and (int(ret['Cores']) != int(ret['Threads']) // 2):
        # Hybrid architecture (SOME Intel 12th gen or later)
        ret |= {
            "Cores": f'{int(ret["Threads"]) - int(ret["Cores"])} P-cores, \
        {2 * int(ret["Cores"]) - int(ret["Threads"])} P-cores ({ret["Cores"]} total)',
            "P-core base frequency": out['Frequency:'],
            "E-core base frequency": out['E-Core Frequency:'],
            "P-core turbo frequency": out['Turbo Clock:'],
            "E-core turbo frequency": out['E-Core Turbo Clock:'],
            "P-core L1 cache": out['Cache L1:'],
            "P-core L2 cache": out['Cache L2:']
        }
        try:
            ret |= {
                "E-core L1 cache": out['E-Core L1:'],
                "E-core L2 cache": out['E-Core L2:']
            }
        except KeyError:
            pass
    else:
        ret |= {
            "Base frequency": out['Frequency:'],
            "Turbo frequency": out['Turbo Clock:'],
            "L1 cache": out['Cache L1:'],
            "L2 cache": out['Cache L2:']
        }
    try:
        ret |= {
            "L3 cache": out['Cache L3:']
        }
    except KeyError:
        pass

    return [r.status_code, ret]


def run(name: str):
    return [get_info(i) for i in search(name)]
