import requests
import urllib.parse


def run(word: str, target_language: str):
	url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

	payload = f"q={urllib.parse.quote(word)}&target={target_language}"
	headers = {
		"content-type": "application/x-www-form-urlencoded",
		"Accept-Encoding": "application/gzip",
		"X-RapidAPI-Key": "496a7e6b29mshac43046c732c619p1d3b0ejsnf33d718129e6",
		"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
	}

	response = requests.request("POST", url, data=payload, headers=headers).json()
	data = response['data']['translations'][0]
	return [data['translatedText'], data['detectedSourceLanguage']]


