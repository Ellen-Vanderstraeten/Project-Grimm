import requests
from bs4 import BeautifulSoup
import re


def saveStory(path, paragraphs):
    """
    Save all paragraphs to a file, and stop when <h2>Anhang</h2> has been reached.
    """
    f = open("Versions/" + path.split("/")[-1] + ".txt", "w")
    for p in paragraphs:
        if p.text.startswith("Anhang"):
            break
        else:
            f.write(p.text)
    f.close()


def mineStory(home, link):
    page = requests.get(home + link)
    pageSoup = BeautifulSoup(page.content, "lxml")
    pageSoup.prettify()
    paragraphs = pageSoup.find_all(["p", "h2"])
    saveStory(link, paragraphs)


def getAllVersionLinks(url):
    r = requests.get(url)
    r.content
    soup = BeautifulSoup(r.content, "lxml")
    soup.prettify()
    links = soup.find_all("a", href=re.compile(r"\/wiki\/.*((1812)|(1815)|(1819)|(1837)|(1840)|(1843)|(1850)|(1857))"))
    return links


def linkIsValid(link):
    return ("Fragment" not in link) and ("Band" not in link)


def main():
    home = "https://de.wikisource.org"
    links = getAllVersionLinks("https://de.wikisource.org/wiki/Kinder-_und_Hausm%C3%A4rchen")
    for link in links:
        hrefText = link["href"]
        if linkIsValid(hrefText):
            print(hrefText)
            mineStory(home, hrefText)

if __name__ == "__main__":
    main()