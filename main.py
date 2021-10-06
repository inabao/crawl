import requests
from bs4 import BeautifulSoup
from constant import *
from spider import *
mainPath = "http://www.zhongyaocai360.com"
mainPage = "/zhongyaodacidian"


def generateAllUrl():
    crawlPage = mainPath + mainPage
    response = requests.get(crawlPage, headers=HEAD)
    response.encoding = "gb2312"
    bs = BeautifulSoup(response.text, features="lxml")
    uls = bs.find_all(attrs={"class": "uzyc"})
    ils = []
    for ul in uls:
        ils.extend(ul.children)
    urls = []
    for il in ils:
        urls.append(mainPath + il.a["href"])
    return urls


if __name__ == '__main__':
    urls = generateAllUrl()
    for url in urls:
        print(getData(url))
