import requests
import re


def search(term: str):
    get = requests.get(f"https://phone-specs-api.azharimm.dev/search?query={term}").json()
    ret = get['data']['phones']
    names = [(i['brand'] + i['phone_name']).lower() for i in ret]
    try:
        if term.lower() in names:
            return ret[names.index(term.lower())]
        length = []
        for i in names:
            length.append(len(i.replace(term, '')))
        if len(length) == 1:
            return ret[length.index(length[0])]
        else:
            return ret[length.index(min(*length))]
    except [IndexError, TypeError]:
        return None


def run(term: str):
    s = search(term)
    if s is None:
        return {
            "Info": "The phone can not be found.",
            "Searched for": term
        }
    get = requests.get(s['detail']).json()
    ret = {
        "Name": f"{get['data']['brand']} {get['data']['phone_name']}",
        "Release date": get['data']['release_date'].replace("Released ", "")
    }
    specifications = get['data']['specifications']
    titles = [i['title'] for i in specifications]

    def specs(i: int):
        return specifications[i]['specs']

    def key(i: int, j: int):
        return specifications[i]['specs'][j]['key']

    def val(i: int, j: int):
        return ", ".join(specifications[i]['specs'][j]['val'])

    idx = titles.index('Body')
    ret |= {"Body": "{}, {}".format(val(idx, 0), val(idx, 1))}
    if key(idx, 2) == "Build":
        ret['Body'] += ", {}".format(re.sub(r'(\w)([A-Z])', r"\1 or \2", val(idx, 2)))
    idx = titles.index('Display')
    ret |= {"Display": "{}, {}, {}".format(val(idx, 0), re.search('.* inches', val(idx, 1)).group(0),
                                           re.search('.* x .* pixels', val(idx, 2)).group(0))}
    if 'Platform' in titles:
        idx = titles.index('Platform')
        if key(idx, 1) == "Chipset":
            # There are some phones that have at least two SoC variants
            # Not sure if this statement can capture those
            try:
                var1, var2 = [], []
                for i in range(1, 4):
                    v = val(idx, i)
                    srch = re.search('.* - (EMEA/LATAM|Global|International|Europe)', v).group(0)
                    var1.append(re.sub(' - (EMEA/LATAM|Global|International|Europe)', '', srch))
                    var2.append(re.sub(' - (USA(/China|)|ROW)', '', v.replace(srch, '')))
                ret |= {"SoC": """\n    {} ({}, {})\n    {} ({}, {})"""
                        .format(*var1, *var2)}
            except AttributeError:
                ret |= {"SoC": "{} ({}, {})".format(*[val(idx, i) for i in range(1, 4)])}
    idx = titles.index('Memory')
    if key(idx, 1) == "Internal":
        ret |= {"RAM and storage": "{}; SD card slot: {}".format(val(idx, 1), val(idx, 0))}
    elif key(idx, 1) == "Phonebook":
        ret |= {"Storage": "{} phonebook entries".format(re.search('[0-9]+', val(idx, 1)))}
    if 'Main Camera' in titles:
        idx = titles.index('Main Camera')
        ret |= {"Main camera": "{} ({})".format(key(idx, 0), val(idx, 0).replace('\n', '; '))}

    if 'Selfie camera' in titles:
        idx = titles.index('Selfie camera')
        ret |= {"Selfie camera": "{} ({})".format(key(idx, 0), val(idx, 0).replace('\n', '; '))}

    idx = titles.index('Battery')
    ret |= {"Battery": "{}".format(val(idx, 0))}
    if len(specs(idx)) > 1 and key(idx, 1) == "Charging":
        ret['Battery'] += "; charging technology: {}".format(val(idx, 1).replace('\n', '; '))

    idx = titles.index('Comms')
    ret |= {"Network": ""}
    net = []
    if val(idx, 0) != "No":
        net.append("{}".format(val(idx, 0)))
    if val(idx, 1) != "No":
        net.append("Bluetooth {}".format(val(idx, 0)))
    idx = titles.index('Network')
    net.append(val(idx, 0))
    ret['Network'] = "; ".join(net)

    return ret
