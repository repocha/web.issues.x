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
        #cmd = 'curl -u tianyin:xuty19850620 -i ' + 'https://api.github.com/repos/' + repo + '/pulls -o tmp/' + raw
        d = json.load(content)
        if len(d) > 0:
          print raw, d[0]['number']
        #time.sleep(0.5)
      except Exception as e:
        print raw, e
    

with open('count.repo') as f:
  for l in f:
    repo = l.strip().split(' ')[0]
    count = int(l.strip().split(' ')[1])
    os.mkdir('issues/' + repo)
    for i in range(count):
      path = 'issues/' + repo + '/' + str(i+1)
      url = 'https://github.com/' + repo.replace('.', '/', 1) + '/pull/' + str(i+1)
      print url
      try:
        with open(path, 'w') as f:
          f.write(urllib2.urlopen(url, timeout=5).read())
        time.sleep(1)
      except Exception as e:
        print e

#get_last_prno('repos_no_check_301.lst')
