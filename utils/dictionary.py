import sys
import urllib.parse
from io import StringIO

import requests as r

old_stdout = sys.stdout

result = {}


def is_word_not_found():
    return (result is None) or ("title" in result and result['title'] == "No Definitions Found")


def get_phonetics():
    if "phonetics" in result:
        try:
            phonetics = list([x["text"] for x in result["phonetics"]])
            print(*phonetics, sep=", ")
        except KeyError:
            return


def get_meanings():
    if "meanings" in result:
        meanings = list([x for x in result["meanings"]])
        for meaning in meanings:
            print(meaning["partOfSpeech"])
            for idx, definition in enumerate(meaning["definitions"]):
                print(f"""{idx + 1}. {definition["definition"]}""")
                if "example" in definition:
                    print(f"""Example: {definition["example"]}""", end="\n\n")
            print("Synonyms: ", end='')
            print(*meaning["synonyms"], sep=", ")
            print("Antonyms: ", end='')
            print(*meaning["antonyms"], sep=', ', end="\n\n")


def get_result(word: str):
    global result
    sys.stdout = out = StringIO()
    try:
        request = r.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + urllib.parse.quote(word))
        result = request.json()[0]
        print(f"**{word}**")
        get_phonetics()
        get_meanings()
    except KeyError:
        print("Word not found")
    sys.stdout = old_stdout
    result = out.getvalue()
    return result


def run(word: str):
    a = get_result(word)
    ret = []
    while len(a) > 2000:
        b = str(result[:2000])
        c = b.rfind("\n")
        ret += [str(result[:c])]
        a = str(result[c + 1:])
    ret += [a]
    return ret
