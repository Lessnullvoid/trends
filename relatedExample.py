
import sys
import json
import xmltodict
from pytrends.request import TrendReq

google_email = "xxx"
google_password = "xxx"

def startTrending(email, password):
    pytrends = TrendReq(email, password)
    hotTrendsPayLoad = {
        "hl": "en-US",
        "geo": "MX",
        "cat": "all"
    }
    getHotTrends(pytrends, hotTrendsPayLoad)


def getHotTrends(pytrends, payload):
    result = pytrends.hottrendsdetail(payload)
    print('Trends Fetched')
    o = xmltodict.parse(result)
    with open('result.json', 'w') as outfile:
        json.dump(o, outfile)


def main():
    if len(sys.argv) >= 3:
        google_email = sys.argv[1]
        google_password = sys.argv[2]
        startTrending(google_email, google_password)
    else:
        print("Please provide google email & password")



if __name__ == '__main__':
  main()
