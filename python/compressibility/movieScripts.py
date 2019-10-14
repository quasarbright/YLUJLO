import time
import re
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from compressionLogic import compressibility

# page = requests.get("https://www.imsdb.com/scripts/Lock,-Stock-and-Two-Smoking-Barrels.html")
# soup = BeautifulSoup(page.content)
# script = str(soup.find('pre'))
html_tag_pattern = r'</?\w*?>'
# script = re.sub(html_tag_pattern, "", script)


def getMovieScript(title):
    prefix = 'https://www.imsdb.com'
    first = title[0].upper()
    if first not in 'qwertyuiopasdfghjklzxcvbnm'.upper():
        url = 'https://www.imsdb.com/alphabetical/0'
    else:
        url = f'https://www.imsdb.com/alphabetical/{first}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    anchor = soup.find('a', string=title)
    if anchor is None:
        return None

    movieURL = prefix + anchor['href']
    # time.sleep(5)
    moviePage = requests.get(movieURL)
    movieSoup = BeautifulSoup(moviePage.content)
    
    scriptAnchor = movieSoup.find('a', string=f'Read "{title}" Script')
    if scriptAnchor is None:
        return None
    
    scriptURL = prefix + scriptAnchor['href']
    # time.sleep(5)
    scriptPage = requests.get(scriptURL)
    scriptSoup = BeautifulSoup(scriptPage.content)
    script = str(scriptSoup.find('pre'))
    if script is None:
        return None

    script = re.sub(html_tag_pattern, "", script)
    return script


def getCompressibility(title):
    script = getMovieScript(title)
    if script is None:
        return None
    
    return compressibility(script)

firsts = 'QWERTYUIOPASDFGHJKLZXCVBNM0'
columns = ['title', 'compressibility']
df = pd.DataFrame(columns=columns)
for first in firsts:
    try:
        letterPage = requests.get(f'https://www.imsdb.com/alphabetical/{first}')
        letterSoup = BeautifulSoup(letterPage.content)
        td = letterSoup.find_all('td', valign='top')[2]
        ps = td.find_all('p')
        for p in ps:
            try:
                title = str(p.a.string)
                scriptCompressibility = getCompressibility(title)
                df = df.append(
                    {'title': title, 'compressibility': scriptCompressibility}, ignore_index=True)
                print(title)
            except:
                continue
    except:
        continue

print(df)
df.to_csv('movie script.csv')
