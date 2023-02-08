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
	try:
		for idx, name in enumerate(names):
			if name.lower() == term.lower():
				return ret[idx]
			if name.lower().startswith(term.lower()) or name.lower().endswith(term.lower()):
				return ret[idx]
		return ret[0]
	except IndexError:
		return None


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
	if item is None:
		return [0, {
			"Info": "The CPU can not be found.",
			"Searched for": term
		}]
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
	igpu = 0
	# General info
	ret = {
		"Name": name,
		"Release date": out['Release Date']
	}
	if 'GPU Variant' in out:
		ret = {
			**ret,
			"Die variant": out['GPU Variant']
		}
	ret = {
		**ret,
		"GPU type": ""
	}
	if out['Memory Size'] == "System Shared":
		igpu = 1
		ret["GPU type"] = "Integrated graphics"
	else:
		ret["GPU type"] = "Discrete graphics"
	ret = {
		**ret,
		"Architecture": out['Architecture'],
		"Fabrication process": out['Process Size']
	}
	if all(key in out for key in ("Width", "Height")):
		ret = {
			**ret,
			"Size": f"{out['Length']} x {out['Width']} x {out['Height']}"
		}
	elif "Length" in out:
		ret = {
			**ret,
			"Length": out['Length']
		}
	if igpu != 0:
		ret = {
			**ret,
			"Slot width": out['Slot Width']
		}
	ret = {
		**ret,
		"Die size": out['Die Size']
	}

	if "Shading Units" in out:
		ret = {
			**ret,
			"Processor": f"{out['Shading Units']} shading units"
		}
	elif "Pixel Shaders" in out and "Vertex Shaders" in out:
		ret = {
			**ret,
			"Shader processors": f"{out['Pixel Shaders']} pixel shaders, {out['Vertex Shaders']} vertex shaders"
		}
	if "SM Count" in out:
		ret['Processor'] += f" in {out['SM Count']} stream processors"
	elif "SMM Count" in out:
		ret['Processor'] += f" in {out['SMM Count']} stream processors"
	elif "Compute Units" in out:
		ret['Processor'] += f" in {out['Compute Units']} compute units"
	ret = {
		**ret,
		"Core config": f"{out['TMUs']} TMUs, {out['ROPs']} ROPs"
	}
	if 'RT Cores' in out:
		ret = {
			**ret,
			"Ray tracing cores": out['RT Cores']
		}
	if 'Tensor Cores' in out:
		ret = {
			**ret,
			"Tensor cores": out['Tensor Cores']
		}
	if 'Base Clock' in out:
		ret = {
			**ret,
			"Base clock": out['Base Clock'],
			"Boost clock": out['Boost Clock']
		}
	else:
		ret = {
			**ret,
			"GPU clock": out['GPU Clock']
		}
	if 'Shader Clock' in out:
		ret = {
			**ret,
			"Shader clock": out['Shader Clock']
		}
	if igpu == 0:
		ret = {
			**ret,
			"Memory": f"{out['Memory Size']} {out['Memory Type']} @ {out['Memory Clock']}, {out['Memory Bus']} bus",
			"Memory bandwidth": out['Bandwidth'],
		}
	ret = {
		**ret,
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

	ret = {
		**ret,
		"TDP": out['TDP'],
		"Theoretical performance": ""
	}
	if 'FP16 (half) performance' in out:
		ret["Theoretical performance"] += f"{out['FP16 (half) performance']} FP16, "
	if 'FP32 (float) performance' in out:
		ret["Theoretical performance"] += f"{out['FP32 (float) performance']} FP32"
		if 'FP64 (double) performance' in out:
			ret["Theoretical performance"] += f", {out['FP64 (double) performance']} FP64"
	elif 'Pixel Rate' in out and 'Vertex Rate' in out:
		ret["Theoretical performance"] += f"{out['Pixel Rate']}, {out['Vertex Rate']}"
	ret = {
		**ret,
		"Feature support": ""
	}
	sp = []
	for i in ["DirectX", "OpenGL", "OpenCL", "CUDA", "Vulkan", "Shader Model"]:
		if i in out and out[i] != "N/A":
			if i == "DirectX":
				fl = soup.find('span', title="DirectX Feature Level").contents[0][1:-1]
				sp.append(f"DirectX {out['DirectX']} (feature level {fl})")
			else:
				sp.append(f"{i} {out[i]}")
	ret['Feature support'] += ", ".join(sp)
	return [r.status_code, ret]


