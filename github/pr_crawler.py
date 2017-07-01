import json
import urllib
import urllib2, base64
import time
import os
import sys
import utils

sys.path.append('..')
from crawler import URLCrawler

#os.mkdir('issues')

urls = []
with open('count.repo') as f:
  for l in f:
    repo = l.strip().split(' ')[0]
    count = int(l.strip().split(' ')[1])

    #iterate from 1 to the lastest count
    for i in range(count):
      path = 'issues/' + repo + '/' + str(i+1)
      #url = 'https://github.com/' + repo.replace('.', '/', 1) + '/pull/' + str(i+1)
      url = utils.gen_prurl(utils.reponame2repourl(repo), str(i+1))
      print url, path
      urls.append((url, path))

crawler = URLCrawler()
urls_tocrawl = crawler.calibrate(urls)
#print len(urls_tocrawl)
crawler.crawl(urls_tocrawl, 0.5)
