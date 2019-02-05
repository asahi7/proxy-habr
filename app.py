from flask import Flask
import requests
import re
from bs4 import BeautifulSoup


app = Flask(__name__)

PROXY_FOR = 'http://habrahabr.ru/'

# Matches all paths and fetches the requested one from the habr's server.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    r = requests.get('{}{}'.format(PROXY_FOR, path))
    text = r.text
    text = swap_habr_links(text, 'http://127.0.0.1:8232')
    alternate_text = append_tm(text)
    return alternate_text


# Alters habr's url links to the address of proxy-server.
def swap_habr_links(text, link):
    p = re.compile(
        r'https?:\/\/(habrahabr.ru|habr.com)',
        re.MULTILINE | re.IGNORECASE)
    text = p.sub(link, text)
    return text


# Appends '™' character to words with length of 6 chars.
# Examines all text within tags in DOM and replaces it with new formatted one.
def append_tm(text):
    soup = BeautifulSoup(text, 'html.parser')
    excluded_tags = [
        'script',
        'svg',
        'html',
        'head',
        'meta',
        'title',
        'link',
        'style',
        'path',
        'br',
        'use',
        'stop',
        'lineargradient',
        'g',
        'symbol',
        'code',
        'pre']
    for tag in soup.find_all(True):
        if tag.name in excluded_tags:
            continue
        for child in tag.children:
            if child.name in excluded_tags:
                continue
            if hasattr(child, 'string') and child.string is not None:
                text = str(child.string)
                newtext = ""
                word = ""
                for c in text:
                    if c.isalpha():
                        word += c
                    else:
                        if len(word) == 6 and c != '™':
                            newtext += word + '™' + c
                        else:
                            newtext += word + c
                        word = ""
                if len(word) != 0:
                    if len(word) == 6:
                        newtext += word + '™'
                    else:
                        newtext += word
                child.string.replace_with(newtext)
    return str(soup)


if __name__ == '__main__':
    app.run(port=8232)
