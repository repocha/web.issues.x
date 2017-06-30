import urllib2
import time
import os
import logging
from lxml.html import fromstring

class URLCrawler():
  """
  Given a bunch of URLs, and crawl them one by one
  """
  def __init__(self, log_file=None, ishtml=True):
    self.ishtml = ishtml
    if log_file != None:
      self.log_file = log_file
      logging.basicConfig(filename=log_file,level=logging.DEBUG)
    else:
      logging.basicConfig(level=logging.DEBUG)

  def calibrate(self, urlpl):
    """urlpl is a list of (u, f) pairs where u is the url to crawl, and f is the dest
    file path; we intentionally do not use dict to keep the crawling order.
    """
    crawled = []
    tocrawl = []
    for pair in urlpl:
      u = pair[0]
      f = pair[1]
      if os.path.exists(f) and os.path.getsize(f) > 0 and self.__validateHTML(f):
        crawled.append((u, f))
      else:
        tocrawl.append((u, f))   
    logging.info('--------------------------------------------------------------------')
    logging.info(' CALIBRATION')
    logging.info('--------------------------------------------------------------------')
    logging.info('#CRAWLED URLS: ' + str(len(crawled)))
    logging.info('#TOCRAWL URLS: ' + str(len(tocrawl)))
    logging.info('--------------------------------------------------------------------')
    return tocrawl

  def __crawl(self, url, dstpath, intv=1):
    """utility function
    """
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url,headers=hdr)
    with open(dstpath, 'w') as f:
      f.write(urllib2.urlopen(req, timeout=5).read())
      time.sleep(intv)

  def __validateHTML(self, htmlpath):
    try:
      with open(htmlpath) as f:
        fromstring(f.read())
      return True
    except:
      return False

  def crawl(self, urlpl, mandatory=False, intv=1):
    """urlpl is a list of (u, f) pairs where u is the url to crawl, and f is the dest
    file path; we intentionally do not use dict to keep the crawling order.
    """
    scnt = 0
    fcnt = 0
    # generate the dirs first
    for pair in urlpl:
      u = pair[0]
      f = pair[1]
      d = f[:f.rfind('/')]
      if os.path.exists(d) == False:
        try:
          os.makedirs(d)
          print 'created dir', d
        except Exception as e:
          logging.error(e)
          logging.error('Fail to mkdir: ' + download_dir)
          return

    for pair in urlpl:
      u = pair[0]
      f = pair[1]
      if mandatory == False and os.path.exists(f):
        logging.info('SKIP (CRAWLED): ' + u)
      else:
        try:
          self.__crawl(u, f, intv)
          logging.info('CRAWLED: ' + u)
          scnt += 1
        except Exception as e:
          logging.error('FAILURE: ' + u)
          logging.error(e)
          fcnt +=1
    logging.info('#Crawled URLs: ' + str(scnt))
    if fcnt > 0:
      logging.info('#Failed URLs: ' + str(fcnt))
