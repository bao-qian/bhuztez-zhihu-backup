import json
from datetime import datetime
import os

import requests

log_file = "{}.log".format(__file__)


def log(message):
    """
    :type message:str
    """
    time_format = "%d-%b %H:%M:%S"
    now = datetime.now().strftime(time_format)
    formatted = "{}: {}".format(now, message)
    print(formatted)
    with open(log_file, "a+", encoding="utf-8") as f:
        f.write(formatted + "\n")


def get(url):
    # add as you wish
    proxies = {
        'http': "",
        'https': "",
    }
    headers = {
        "User-Agent": ",
        "Cookie": '',
    }
    r = requests.get(url, proxies=proxies, headers=headers)
    return r


def save_content(path, content):
    with open(path, "w+", encoding="utf-8") as f:
        parsed = json.dumps(content, indent=4, ensure_ascii=False)
        f.write(parsed)


def download_api(api_url, api_name):
    ended = False
    offset = 0
    while not ended:
        url = "{}?include=data%5B*%5D.content&limit=20&offset={}".format(
            api_url,
            offset
        )
        ended, content = _download_api(url)
        filename = "{}_{}.json".format(api_name, offset)
        log(content)
        path = os.path.join(api_name, filename)
        save_content(path, content)
        offset += 20


def _download_api(url):
    log("Downloading <{}>".format(url))
    r = get(url)
    if r.status_code == 200:
        log("Download <{}> succeed".format(url))
        parsed = r.json()
        ended = parsed["paging"]["is_end"]
        return ended, parsed
    else:
        log("Download <{}> failed".format(url))
        log("Error detail: <{}>".format(r.text))
        return True, ""


def data_from_api_name(api_name):
    files = os.listdir(api_name)
    answers = []
    for f in files:
        path = os.path.join(api_name, f)
        a = data_from_file(path)
        answers = answers + a
    return answers


def data_from_file(path):
    log("Loading <{}>".format(path))
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        parsed = json.loads(content)
        data = parsed["data"]
        return data


def download_answers():
    url = "https://www.zhihu.com/api/v4/members/bhuztez/answers"
    name = "answers"
    download_api(url, name)
    l = data_from_api_name(name)
    save_content("{}.json".format(name), l)


def download_articles():
    url = "https://www.zhihu.com/api/v4/members/bhuztez/articles"
    name = "articles"
    download_api(url, name)
    l = data_from_api_name(name)
    save_content("{}.json".format(name), l)


# download_answers()
download_articles()