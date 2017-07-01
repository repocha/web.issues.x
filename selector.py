import string
import random
from kwfilter import KWFilter

def threads_select(threads, xfilt):
  """
  Give a list of threads and select the interesting ones among them
  """
  res = []
  for t in threads:
    if interested(t, xfilt):
      res.append(t)
  #random.shuffle(res)
  return res

def interested(thread, xfilt):
  """success: return the url
  failure: return None
  """
  if xfilt.contains(thread.question.content):
    #print thread.question.content
    return True
  # check if a thread has answers. only check its answers if it has any
  if thread.answers != None:
    for answer in thread.answers:
      if xfilt.contains(answer.content):
        #print answer.content
        return True
  return False
