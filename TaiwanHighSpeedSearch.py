import urllib.request
import urllib.parse
from lxml import etree

request = urllib.request.Request("http://www.thsrc.com.tw/tw/TimeTable/SearchResult");
request.add_header("User-Agent",
"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36");

form_data = {
    "StartStation":"f2519629-5973-4d08-913b-479cce78a356",
    "EndStation":"977abb69-413a-4ccf-a109-0272c24fd490",
    "DepartueSearchDate":"2018/12/10",
    "DepartueSearchTime":"05:00",
    "SearchType":"S",
}

form_data = urllib.parse.urlencode(form_data).encode("utf-8");
response = urllib.request.urlopen(request, data=form_data)
html = response.read()
#print(html)


'''
Process all image files
'''
page = etree.HTML(html)
count = 0
for url in page.xpath(u"//img/@src"):
    if True:
        try:
            image_request = urllib.request.Request("http://www.thsrc.com.tw"+url)
            image_response = urllib.request.urlopen(image_request)
            image_data = image_response.read()
        except Exception as e:
            print(e)
            continue

        count = count + 1
        filename = str(count) + ".jpg"
        pic_out = open(filename, 'wb')
        pic_out.write(image_data)
        pic_out.close()