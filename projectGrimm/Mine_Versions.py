import requests
from bs4 import BeautifulSoup
import re
import os
import io

'''Get the right links (filter on the dates of the different editions)'''
def getAllVersionLinks(url):
    r = requests.get(url)
    r.content
    soup = BeautifulSoup(r.content, "lxml")
    soup.prettify()
    links = soup.find_all("a", href=re.compile(r"\/wiki\/.*((1812)|(1815)|(1819)|(1837)|(1840)|(1843)|(1850)|(1857))"))
    return links

'''Still too many links. Need to filter out those links which contain 'Fragment and 'Band' ' '''
def linkIsValid(link):
    if ("Fragment" not in link) and ("Band" not in link):
        return link

def saveStory(path, paragraphs):
'''Save all paragraphs to a file, use name of link for name for text file. 
Stop when <h2>Anhang</h2>, <h2>Anmerkungen</h2> or <h2>Navigationsmenü</h2> has been reached.''' 
    f = io.open("Versions/" + path.split("/")[-1] + ".txt", "w", encoding="utf-8")
    for p in paragraphs:
        if p.text.startswith("Anhang"):
            break
        elif p.text.startswith("Anmerkungen"):
            break
        elif p.text.startswith("Navigationsmenü"):
            break
        else:
            f.write(p.text)
    f.close()


def mineStory(home, link):
    page = requests.get(home + link)
    pageSoup = BeautifulSoup(page.content, "lxml")
    pageSoup.prettify()
    for PageNumber in pageSoup.find_all("span"):
        PageNumber.replace_with("")
    paragraphs = pageSoup.find_all(["p", "h2"])
    saveStory(link, paragraphs)


def main():
    home = "https://de.wikisource.org"
    links = getAllVersionLinks("https://de.wikisource.org/wiki/Kinder-_und_Hausm%C3%A4rchen")
    for link in links:
        hrefText = link["href"]
        if linkIsValid(hrefText):
            print(hrefText)
            mineStory(home, hrefText)

main()