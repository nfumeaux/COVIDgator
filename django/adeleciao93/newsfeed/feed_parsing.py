import requests
from bs4 import BeautifulSoup
import re

#url = 'http://feeds.nature.com/nature/rss/current?x=1'
url ='http://feeds.bbci.co.uk/news/world/rss.xml'

resp = requests.get(url)

soup = BeautifulSoup(resp.content, features='xml')

#find titles for filtering
relevant_soup = soup.find_all('title', string=re.compile('virus'))
relevant_soup2 = soup.find_all('title', string=re.compile('COVID'))

relevant_titles = []
for title in relevant_soup:
    relevant_title = title.text
    relevant_titles.append(relevant_title)

for title in relevant_soup2:
    relevant_title = title.text
    relevant_titles.append(relevant_title)

set_titles = set(relevant_titles)
list_titles = list(set_titles)

#find all items and creare list of dictionaries
items = soup.find_all('item')

news_items = []

for item in items:
    news_item = {}
    news_item['title'] = item.title.text
    news_item['link'] = item.link.text
    news_item['source'] = url
    news_items.append(news_item)

#filtering for relevant titles
news_items_filt = [d for d in news_items if d['title'] in list_titles]


#translate to sql format
# for news_item in news_items_filt:
#     placeholders = ', '.join(['%s'] * len(news_item))
#     columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in news_item.keys())
#     values = ', '.join("'" + str(x).replace("'s", ' s') + "'" for x in news_item.values())
#     sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('NewsTable', columns, values)
#     #print(sql)
#
#     f = open("nature.sql", "a")
#     f.write(sql + '\n')


