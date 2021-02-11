from bs4 import BeautifulSoup
from pandas import DataFrame
from requests import get
from urllib.request import urlparse

url = 'https://lyricstranslate.com/en/translations/15/328/none/none/none/0/0/0/0'

for each_page in range(0, 10):

    page = get(url, params=dict(
        page=each_page
    ))

    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table')

    records = []
    for tr in table.findAll("tr"):
        trs = tr.findAll("td")
        record = []
        for each in trs:
            try:
                link = each.find('a')['href']
                text = each.text
                record.append(text)
                target_url = '{uri.scheme}://{uri.netloc}{path}'.format(
                    uri=urlparse(url), path=link)
                record.append(target_url)

                # YOLO
                target_page = get(target_url)
                target_soup = BeautifulSoup(target_page.text, "html.parser")

                lyrics = target_soup.find_all('div', {'class': 'ltf'})
                chinese_lyrics = lyrics[0].text
                english_lyrics = lyrics[1].text

                record.append(chinese_lyrics)
                record.append(english_lyrics)
            except:
                continue
        records.append(record)

    df = DataFrame(data=records[1:], columns=["Artist", "Artist Link", "Song",
                                              "Song Link", "Chinese Lyrics", "English Lyrics", "Author", "Author Link"])
    df.to_html('data-{0}.html'.format(each_page))
    df.to_csv('data-{0}.csv'.format(each_page))
    df.to_excel('data-{0}.xls'.format(each_page))
