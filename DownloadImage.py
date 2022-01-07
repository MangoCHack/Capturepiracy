import csv
import urllib.request
import os
import re

def clean_text(inputString):
  text_rmv = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’· ]', '', inputString)
  return text_rmv

with open('.\\CrawlDB\\CrawlDB.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for data in reader:
        if list(data.keys()) == list(data.values()):
            continue
        #key : ['hosturl', 'webtoonName', 'crawltime', 'updatetime', 'episode', 'file_urls', 'extension']
        data["webtoonName"] = clean_text(data["webtoonName"])
        try:
            if not os.path.exists(f'.\\data\\{data["webtoonName"]}'):
                os.makedirs(f'.\\data\\{data["webtoonName"]}')
        except Exception as e:
            print(e)
            print(data['webtoonName'])
            continue
        try:
            os.system(f'curl {data["file_urls"]} -o .\\data\\{data["webtoonName"]}\\{data["hosturl"]}.{data["extension"]}')
        except Exception as e:
            print(data["hosturl"],data["file_urls"])
            print(e)


        
