import certifi
import urllib3
import urllib.request


url = "https://www.cnyes.com/twstock/sec_quote.aspx?code=FTW50"
#http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
#req = http.request("GET", url)
#html = urllib3.urlopen(req)

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as f:
    print(f.read().decode('utf-8'))






