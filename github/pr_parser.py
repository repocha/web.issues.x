from lxml.html import fromstring
import logging

import sys
sys.path.append('..')
from post import Post
from post import Thread

def parsePRHTML(htmlstr, orgurl=None):
  """parse a PR page
  Return a Thread object
  """
  thread = Thread()
  try:
    doc = fromstring(htmlstr)
    thread.stat = __getstat(doc)
    thread.title = __gettitle(doc)
    thread.url = orgurl

    first = True
    # we only care the content of the comments
    for comment in doc.find_class('comment-body'):
      if first == True: 
        # the original post
        first = False
        content = __norm(comment.text_content())
        thread.question = Post(None, None, thread.title, content)
      else:
        # add into answers 
        content = __norm(comment.text_content())
        thread.answers.append(Post(None, None, thread.title, content))
    return thread
  except Exception as e:
    url = orgurl if orgurl != None else ''
    logging.error('FAILURE: ' + url + '. ' + str(e))
    return None


def __getstat(doc):
  for s in doc.find_class('State'):
    return __norm(s.text_content())

def __gettitle(doc):
  for t in doc.find_class('js-issue-title'):
    return __norm(t.text_content())

def __norm(tstr):
  return tstr.encode('utf-8').replace('\n', ' ').replace('\r', '').strip()

def parse_prs(prl):
  thds = []
  for prp in prl:
    thds.append(parsePRHTML(prp[1], prp[0]))
  return thds
