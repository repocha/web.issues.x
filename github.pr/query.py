import os
import utils
import pr_parser
import pr_loader

import sys
sys.path.append('..')
import selector
from kwfilter import KWFilter

def queryall(prs_dir):
  hit = 0
  cs = [['check', 'style']]
  with open('kw.checks.lst') as f:
    for l in f:
      l = l.strip()
      if l.startswith('#') == False:
        cs.append(l.split(' '))
  kwfilt = KWFilter(cs)
  for repo in os.listdir(prs_dir):
    prs = pr_loader.load_prs(os.path.join(prs_dir, repo))
    for pr in prs:
      url = pr[0]
      cnt = pr[1]
      try:
        t = pr_parser.parsePRHTML(cnt, url)
        if t != None and selector.interested(t, kwfilt):
          hit += 1
          print url, t.title
      except Exception as e:
        print e
        continue
  kwfilt.print_kw_matches()
  print 'HIT:', hit

def query(prs_dir, repo_name):
  cs = [['check', 'style']]
  #with open('kw.checks.lst') as f:
  #  for l in f:
  #    l = l.strip()
  #    if l.startswith('#') == False:
  #      cs.append(l.split(' '))
  kwfilt = KWFilter(cs)
  #prs = pr_loader.load_prs('tests_aggr/alibaba.dubbo')
  #prs = pr_loader.load_prs('tests_aggr/google.guava')
  prs = pr_loader.load_prs(os.path.join(prs_dir, repo_name))
  for pr in prs:
    url = pr[0]
    cnt = pr[1]
    try:
      t = pr_parser.parsePRHTML(cnt, url)
      if t != None and selector.interested(t, kwfilt):
        print url, t.title
    except Exception as e:
      print e
      continue

if __name__ == "__main__":
  """
  if len(sys.argv) != 2:
    print '[usage] python query.py $repo_name'
  else:
    query('tests_aggr', sys.argv[1])
  """
  queryall('tests_aggr')
