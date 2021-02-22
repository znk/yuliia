from bs4 import BeautifulSoup as document
from pandas import DataFrame
from requests import get
from urllib.request import urljoin

url = 'https://lyricstranslate.com/en/translations/15/328/none/none/none/0/0/0/0'

records = []
for page_index in range(0, 18):
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

        record.append(
            {'chinese': to_collect[0].text, 'english': to_collect[1].text})
    records.append(record)

flat_records = [item for sublist in records for item in sublist]

df = DataFrame(flat_records)
df.to_html('data.html', index_names=False)
df.to_csv('data.csv')
