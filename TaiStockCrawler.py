import certifi
import urllib3
import urllib.request
from lxml import etree


url = "https://www.cnyes.com/twstock/sec_quote.aspx?code=FTW50"
url = "https://www.cnyes.com/twfutures/quote_future.aspx"
url = "http://www.stockq.org/index/TWSE.php"
url = "http://www.twse.com.tw/zh/page/trading/indices/MI_5MINS_HIST.html"
#http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
#req = http.request("GET", url)
#html = urllib3.urlopen(req)

req = urllib.request.Request(url)
req.add_header("User-Agent",
"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36");

form_data = {
    "yy":"2018",
    "mm":"11"
}

html = None
form_data = urllib.parse.urlencode(form_data).encode("utf-8");
with urllib.request.urlopen(req, data=form_data) as f:
    html = f.read()

page = etree.HTML(html)
for str in page.xpath(u"//tr[@class='row2']/descendant::text()"):
    print(str)


##############################################


import requests
from bs4 import BeautifulSoup

symbol = 'GOOG'.lower()
url_template = "https://www.nasdaq.com/symbol/{symbol}/historical"
url = url_template.format(symbol=symbol)

rs = requests.session()
r = rs.get(url)
soup = BeautifulSoup(r.text, 'lxml')
params = soup.select('#getFile input')

timeframe = '{timestr}|true|{symbol}'.format(timestr='3m', symbol=symbol.upper())

payload = {}
for tag in params:
    if tag['name'] != 'ctl00$quotes_content_left$submitString':
        payload[tag['name']] = tag['value']
    else:
        payload[tag['name']] = timeframe

r = rs.post(url, data=payload, verify=False)
print(r.text)

rows = r.text.split("\r\n")
columns = []
groups = []
for group in rows[0].split(','):
    #groups.append([eval(group)])
    columns.append(eval(group))

import re
pattern = re.compile("^\s+$")

for i in range(2, len(rows)-1):
    groups.append([])
    for group in rows[i].split(','):
        groups[i-2].append(eval(group))

import pandas as pd
df = pd.DataFrame(groups, columns=columns)