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





