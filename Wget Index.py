import os
import re
from requests import get
from bs4 import BeautifulSoup as Soup

URL = input("Enter The URL:- ")
EXP = input("Enter The EXP:- ")


def list_dir(URL):
    page = get(URL).text
    soup = Soup(page, "html.parser")
    links = soup.findAll("a")
    links = [link["href"] for link in links]
    if links[0] == "../":
        return links[1:]
    else:
        return links


def search(EXP, URL):
    regex = re.compile(EXP)
    links = list_dir(URL)
    match = []
    for link in links:
        if regex.match(link):
            match.append(link)
        if link.endswith("/"):
            match.extend(search(EXP, URL+link))
    return match


# search
match = search(EXP, URL)

# save
fhand = open("links.txt", "w")
for link in match:
    fhand.write(link+"\n")
fhand.close()

# download
for link in match:
    os.system(f"wget -c {link}")
