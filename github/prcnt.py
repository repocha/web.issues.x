import json
import urllib
import urllib2, base64
import time
import os
import subprocess

username = ""
password = ""

def get_last_prno(repo_lst):
  with open(repo_lst) as f:
    for l in f:
      raw = l.strip()
      repo = raw.replace('.', '/', 1)
      try:   
        request = urllib2.Request('https://api.github.com/repos/' + repo + '/pulls')
        base64string = base64.b64encode('%s:%s' % (username, password))
        request.add_header("Authorization", "Basic %s" % base64string)   
        content = urllib2.urlopen(request)
        d = json.load(content)
        if len(d) > 0:
          print raw, d[0]['number']
        #time.sleep(0.5)
      except Exception as e:
        print raw, e

if __name__ == "__main__":    
  get_last_prno('repos.lst')
