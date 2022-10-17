from bs4 import BeautifulSoup
import requests
import lxml
import re
import datetime
from datetime import datetime


# to do make function:
#     -> fun()1 = make request save into BS obj
#      |---> fun()2 = for every catergory(politcs, sports, culture) make a new fun to scrape -> save (title, summary, link to article)
#        |---> fun()3 = format the article into text block



def get_requests(url):
    if url.startswith('https://www.zdf.de/nachrichten'):
        page = requests.get(url).text
        return BeautifulSoup(page, 'lxml')
    else:
        return None

# get all article titles from a specific section -> creates a seperate heads obj
def heads(sect):
    soup = get_requests(r'https://www.zdf.de/nachrichten/'+sect)
    grid = soup.find('section', attrs={'class': 'section b-content-teaser-list b-news-index'})
    articles = grid.find_all('article')
    d = {}
    for article in articles:
        link = 'https://www.zdf.de'+article.div.find('div', attrs={'class': re.compile(r'^box m-tags')}).h3.a['href']

        #filter live tickers:
        if link.startswith('https://www.zdf.de/nachrichten'):
            main_header = article.div.find('div', attrs={'class': re.compile(r'^box m-tags')}).h3.find('span').text.strip('\n')
            spec_header = " ".join(article.div.find('div', attrs={'class': re.compile(r'^box m-tags')}).a.text.strip('\n').replace('\xa0','').split())
            d[link] = [main_header, spec_header]
        else:
            continue

    return d

# article obj
def article(link):
    soup = get_requests(link)
    if type(soup)==str:
        return False
    p_text = []
    rest = {}
    try:
        for txt in soup.find_all('div', attrs={'class':['cell large-8 large-offset-2','large-8 large-offset-2 x-end']}):
            if txt.p:
                p_text.append(clean_text(txt.p))
            elif txt.h2:
                p_text.append(clean_text((txt.h2)).upper())
    except AttributeError:
        pass
    try:
        rest['titles'] = [clean_text(x) for x in soup.find('h2', attrs={'class':'big-headline'}).contents if clean_text(x) and clean_text(x)!=':']
        rest['date'] = datetime.strptime(soup.time['datetime'].replace('T', ' ')[:19], '%Y-%m-%d %H:%M:%S')
        rest['link'] = link
    except AttributeError:
        pass

    try:
        source = soup.find('span', attrs={'class': 'news-source'})
        rest['source'] = clean_text(source).replace('Quelle:', '')
    except AttributeError:
        source = None
    try:
        author = soup.find('div',attrs={'class':'author-wrap'}).div.span
        rest['author'] = clean_text(author)
    except AttributeError:
        author = None

    return rest, p_text

def clean_text(obj):
    obj = obj.text
    objc = ' '.join(obj.replace('\n',' ').replace('\xa0',' ').split())
    if len(obj)>1:
        return objc
    else:
        return False
