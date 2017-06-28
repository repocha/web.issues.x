import urllib2
import time
import os
from lxml.html import fromstring

def crawl(url, dstpath, intv=2):
  """
  Utility function
  """
  if os.path.exists(dstpath):
    if validate(dstpath):
      print 'SKIP (CRAWLED): ', url
      return
    else:
      print 'CORRUPTED: ', url
      os.remove(dstpath)
  with open(dstpath, 'w') as of:
    of.write(urllib2.urlopen(url, timeout=5).read())
    time.sleep(intv)

def validate(htmlpath):
  try:
    with open(htmlpath) as f:
      fromstring(f.read())
    return True
  except:
    return False

class Crawler:
  """
  The base class for crawler
  """
  def __init__(self, odir, olog):
    self.output_dir = odir
    self.output_log = olog

  def crawl(self):
    """
    Crawling stuff and output to the dir
    """
    pass

  def write2log(self):
    pass

class URLCrawler(Crawler):
  """
  Given a bunch of URLs, and crawl them all
  """
  def __init__(self, urls, odir, olog):
    self.output_dir = odir
    self.output_log = olog
    self.urls = urls

  def calibrate(self):
    crawled = []
    tocrawl = []
    for f in os.listdir(self.output_dir):
      if os.path.getsize(os.path.join(self.output_dir, f)) > 0:
        crawled.append(f) 
    for url in self.urls:
      if self.url2fname(url) not in crawled:
        tocrawl.append(url)
    print '--------------------------------------------------------------------'
    print ' CALIBRATION'
    print '--------------------------------------------------------------------'
    #print 'URL#1:        ', crawled[0]
    #print 'URL#2:        ', crawled[1]
    #print 'URL#3:        ', crawled[2]
    #print 'URL#4:        ', crawled[3]
    #print '--------------------------------------------------------------------'
    print '#CRAWLED URLS:', len(crawled)
    print '#TOCRAWL URLS:', len(tocrawl)
    print '--------------------------------------------------------------------'
    return tocrawl

  def crawl(self):
    for url in self.urls:
      try:
        crawl(url, os.path.join(self.output_dir, self.url2fname(url)))
        print 'CRAWLED: ', url
      except:
        print "FAILURE:", url

  def url2fname(self, url):
    return url[url.rfind('/') + 1:]

