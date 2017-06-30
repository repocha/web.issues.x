import os
import sys
import string
import random
from kwfilter import KWFilter
from kwfilter import TagFilter
from util import dedup
import logging

def threads_select(threads, xfilt):
  """
  Give a list of threads and select the interesting ones among them
  """
  res = []
  for thread_key in threads:
    if __interested(threads[thread_key], xfilt):
      res.append(threads[thread_key].url)
  random.shuffle(res)
  return res


def dir_select(dirp, xfilt, fparse, known=None):
  """
  Select the files in $dirp that is interesting.
  Each file is assumed to be parsed to a Thread object by $fparse
  """
  res = []
  for f in os.listdir(dirp):
    ppath = os.path.join(dirp, f)
    thread = fparse(ppath)
    logging.debug(thread)
    if thread == None: #parsing failure
      continue
    if __interested(thread, xfilt):
      url = thread.url
      if known != None and url in known:
        continue
      logging.debug('FOUND URL: ' + url)
      res.append(url)
  dres = dedup(res)
  random.shuffle(dres)
  return dres

def __interested(thread, xfilt):
  """
  Success: return the url
  Failure: return None
  """
  if thread.stat == 'open':
    # We only focus on 'closed' cases or 'NA' cases in the mailing list
    return False
  if isinstance(xfilt, KWFilter):
    # check if thread.question is None. there can be cases that a thread's question
    # is on the other mbox file that is not processed 
    if thread.question != None and xfilt.contains(thread.question.content):
      return True
    # check if a thread has answers. only check its answers if it has any
    if thread.answers != None:
      for answer in thread.answers:
        if xfilt.contains(answer.content):
          return True
  elif isinstance(xfilt, TagFilter):
    if xfilt.contains(thread.tags):
      return True
  return False
