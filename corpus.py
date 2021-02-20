from bs4 import BeautifulSoup as document
from pandas import DataFrame
from requests import get
from urllib.request import urljoin

url = 'https://lyricstranslate.com/en/translations/15/328/none/none/none/0/0/0/0'

records = []
for page_index in range(0, 1):
    page = get(url, params={'page': page_index})
    doc = document(page.text, "html.parser")

    links = [urljoin(url, a['href'])
             for a in doc.select('td[class=ltsearch-songtitle] a[href]')]

    record = []
    for link in links:
        link_page = get(link).text
        link_doc = document(link_page, "html.parser")

        to_collect = link_doc.select('div[class=ltf]')

        if len(to_collect) != 2:
            continue

        record.append(([to_collect[0].text, to_collect[1].text]))
    records.append(record)

df = DataFrame(records, columns=["chinese", "english"])
df.to_html('data.html', index_names=False)
df.to_csv('data.csv')
