import utils
import pr_parser
import pr_loader

import sys
sys.path.append('..')
import selector
from kwfilter import KWFilter

cs = [['check', 'style']]
#with open('kw.checks.lst') as f:
#  for l in f:
#    l = l.strip()
#    if l.startswith('#') == False:
#      cs.append(l.split(' '))
kwfilt = KWFilter(cs)

hit = 0
#prs = pr_loader.load_prs('tests_aggr/alibaba.dubbo')
prs = pr_loader.load_prs('tests_aggr/google.guava')
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
