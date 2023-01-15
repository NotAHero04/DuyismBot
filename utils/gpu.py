import requests

from bs4 import BeautifulSoup


def search(term: str):
    get = requests.get(f"https://www.techpowerup.com/gpu-specs/?ajaxsrch={term}")
    soup = BeautifulSoup(get.text, "html.parser")
    results = soup.find_all('a', href=True)
    names = [i.contents[0] for i in results]
    links = [i['href'] for i in results]
    ret = list(zip(names, links))
    # Now, we need to get the right result
    for idx, name in enumerate(names):
        if name.lower() == term.lower():
            return ret[idx]
        if name.lower().startswith(term.lower()) or name.lower().endswith(term.lower()):
            return ret[idx]
    return ret[0]


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
    x = soup.find_all('dt')
    x1 = process(x)
    y = soup.find_all('dd')
    y1 = process(y)
    out = dict(zip(x1, y1))
    # General info
    ret = {
        "Name": name,
        "Release date": out['Release Date'],
        "Die variant": out['GPU Variant'],
        "Architecture": out['Architecture'],
        "Fabrication process": out['Process Size']
    }
    if all(key in out for key in ("Width", "Height")):
        ret |= {"Size": f"{out['Length']} x {out['Width']} x {out['Height']}"}
    elif "Length" in out:
        ret |= {"Length": out['Length']}
    ret |= {
        "Slot width": out['Slot Width'],
        "Die size": out['Die Size'],
        "Processor": f"{out['Cores']} cores"
    }
    if "SM Count" in out:
        ret['Processor'] += f" in {out['SM Count']} stream processors"
    elif "SMM Count" in out:
        ret['Processor'] += f" in {out['SMM Count']} stream processors"
    elif "Compute Units" in out:
        ret['Processor'] += f" in {out['Compute Units']} compute units"
    ret |= {"Core config": f"{out['TMUs']} TMUs, {out['ROPs']} ROPs"}
    if 'RT Cores' in out:
        ret |= {"Ray tracing cores": out['RT Cores']}
    if 'Tensor Cores' in out:
        ret |= {"Tensor cores": out['Tensor Cores']}
    if 'Base Clock' in out:
        ret |= {
            "Base clock": out['Base Clock'],
            "Boost clock": out['Boost Clock']
        }
    else:
        ret |= {"GPU clock": out['GPU Clock']}
    if 'Shader Clock' in out:
        ret |= {"Shader clock": out['Shader Clock']}
    ret |= {
        "Memory": f"{out['Memory Size']} {out['Memory Type']} @ {out['Memory Clock']}, {out['Memory Bus']} bus",
        "Memory bandwidth": out['Bandwidth'],
        "Interface": out['Bus Interface'],
        "Cache": ""
    }
    if 'L0 Cache' in out:
        ret['Cache'] += f"{out['L0 Cache']} L0, "
    if 'L1 Cache' in out:
        ret['Cache'] += f"{out['L1 Cache']} L1, {out['L1 Cache']} L2"
        if 'L3 Cache' in out:
            ret['Cache'] += f", {out['L3 Cache']} L3"
    else:
        ret['Cache'] += "N/A"

    ret |= {
        "TDP": out['TDP'],
        "Theoretical performance": ""
    }
    if 'FP16 (half) performance' in out:
        ret["Theoretical performance"] += f"{out['FP16 (half) performance']} FP16, "
    ret["Theoretical performance"] += f"{out['FP32 (float) performance']} FP32"
    if 'FP64 (double) performance' in out:
        ret["Theoretical performance"] += f", {out['FP64 (double) performance']} FP64"
    fl = soup.find('span', title="DirectX Feature Level").contents[0][1:-1]
    ret |= {
        "Feature support": f"DirectX {out['DirectX']} (feature level {fl}), OpenGL {out['OpenGL']}, Vulkan {out['Vulkan']}, Shader Model {out['Shader Model']}"
    }

    return [r.status_code, ret]


def run(name: str):
    return get_info(search(name))
