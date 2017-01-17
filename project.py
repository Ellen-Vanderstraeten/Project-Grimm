import requests
from bs4 import BeautifulSoup
from lxml import html
import re 

url = "https://de.wikisource.org/wiki/Kinder-_und_Hausm%C3%A4rchen" 

r = requests.get(url)
r.content
soup = BeautifulSoup(r.content, "lxml")
soup.prettify()

links = soup.find_all("a", href=re.compile(r"\/wiki\/.*((1812)|(1815)|(1819)|(1837)|(1840)|(1843)|(1850)|(1857))"))
#still too many result, eliminate those with (Band).
'''
f = open("links.txt", "wt") #to check if it are the right links that are being filtered.
f.write(str(links))
f.close()
'''

for link in links:
	hrefText = link["href"]
	page = requests.get("https://de.wikisource.org" + hrefText)
	pageSoup = BeautifulSoup(page.content, "lxml")
	pageSoup.prettify()
	paragraf= pageSoup.find_all("p")
	f = open("page1.txt", "wt")
	f.write(str(paragraf))
	f.close()
