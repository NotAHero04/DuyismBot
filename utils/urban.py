import requests
import re

def run(word: str, page: int = 1):
    url = "https://api.urbandictionary.com/v0/define"

    querystring = {"term": word, "page": page}

    ret = []
    r = requests.request("GET", url, params=querystring).json()['list']

    for i, d in enumerate(r):
        ret.append([d['word'], d['thumbs_up'], d['thumbs_down'], d['author'], d['definition'], d['example'],
                d['written_on']])

    return ret

def get_def_count(word: str):
    url = "https://www.urbandictionary.com/define.php"
    querystring = {"term": word}
    r = requests.request("GET", url, params=querystring)
    f = re.findall("page=[0-9]{1,}", r.text)
    if len(f) == 0:
        r2 = requests.request("GET", url, params=querystring)
        f2 = r2.text.count("Flag this definition")
        return f2
    else:
        page = int(f[-1][5:])
        querystring = {"term": word, "page": page}
        r2 = requests.request("GET", url, params=querystring)
        f2 = r2.text.count("Flag this definition")
        return page * 7 - 7 +f2
