import csv
import re

with open('items.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile)
  urls = []
  for row in reader:
    link = row[2]
    m = re.findall('http://(.+?)/', link)
    m = ''.join(m)
    # print m
    urls.append(m)


  urls = list(set(urls))
  print urls
  print len(urls)

  f = open('links.txt', 'w+')
  for url in urls:
  	f.write(url + '\n')
  f.close()

csvfile.close()