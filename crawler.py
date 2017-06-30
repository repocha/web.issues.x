import urllib2
import time
import os
import logging
from lxml.html import fromstring

def crawl(url, dstpath, intv=1):
  """
  Utility function
  """
  hdr = {'User-Agent': 'Mozilla/5.0'}
  req = urllib2.Request(url,headers=hdr)
  with open(dstpath, 'w') as of:
    of.write(urllib2.urlopen(req, timeout=5).read())
    time.sleep(intv)

class URLCrawler():
  """
  Given a bunch of URLs, and crawl them one by one
  """
  def __init__(self, log_file=None):
    if log_file != None:
      self.log_file = log_file
      logging.basicConfig(filename=log_file,level=logging.DEBUG)
    else:
      logging.basicConfig(level=logging.DEBUG)

  def calibrate(self, urls, download_dir):
    crawled = []
    tocrawl = []
    for f in os.listdir(download_dir):
      if os.path.getsize(os.path.join(download_dir, f)) > 0:
        crawled.append(f) 
    for url in urls:
      if self.url2fname(url) not in crawled:
        tocrawl.append(url)
    logging.info('--------------------------------------------------------------------')
    logging.info(' CALIBRATION')
    logging.info('--------------------------------------------------------------------')
    #print 'URL#1:        ', crawled[0]
    #print 'URL#2:        ', crawled[1]
    #print 'URL#3:        ', crawled[2]
    #print 'URL#4:        ', crawled[3]
    #print '--------------------------------------------------------------------'
    logging.info('#CRAWLED URLS: ' + str(len(crawled)))
    logging.info('#TOCRAWL URLS: ' + str(len(tocrawl)))
    logging.info('--------------------------------------------------------------------')
    return tocrawl

  def crawl(self, urls, download_dir, mandatory=False):
    scnt = 0
    fcnt = 0
    if os.path.exists(download_dir) == False:
      try:
        os.makedirs(download_dir)
      except Exception as e:
        logging.error(e)
        logging.error('Fail to mkdir: ' + download_dir)
        return
    for url in urls:
      dstpath = os.path.join(download_dir, self.url2fname(url))
      if mandatory == False and os.path.exists(dstpath):
        logging.info('SKIP (CRAWLED): ' + url)
      else:
        try:
          crawl(url, dstpath)
          logging.info('CRAWLED: ' + url)
          scnt += 1
        except Exception as e:
          logging.error('FAILURE: ' + url)
          logging.error(e)
          fcnt +=1
    logging.info('#Crawled URLs: ' + str(scnt))
    if fcnt > 0:
      logging.info('#Failed URLs: ' + str(fcnt))

  def url2fname(self, url):
    return url[url.rfind('/') + 1:]

