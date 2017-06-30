import json

class Post:
  """A class representing a post. Each Post object has the sender's email addr 
  (from_addr - string), the receiver's email addr (to - string), the subject 
  of the post (title - string), and the content of the email (content - string)
  It could be used to express an email or a post on a forum
  """
  def __init__(self, from_addr, to, title, content, time='', url=None):
    self.from_addr = from_addr
    self.to = to
    self.title = title
    self.content = content
    self.time = time
    self.url = url

  def tojson(self):
    json = {}
    json['from_addr'] = self.from_addr
    json['to'] = self.to
    json['title'] = self.title
    json['content'] = self.content
    json['time'] = self.time
    json['url'] = self.url
    return json

  def fromjson(self, jp):
    self.from_addr = jp['from_addr']
    self.to = jp['to']
    self.title = jp['title']
    self.content = jp['content']
    self.time = jp['time']
    self.url = jp['url']

  def __str__(self):
    #print 'from:    ', self.from_addr
    #print 'title:   ', self.title
    #print 'content: ', self.content
    return self.from_addr + ": " + self.title + "\n" + '--------------\n' + self.content 

class Thread:
  """
  A class representing thread. Each Thread object has the subject of the first post 
  (title - string), the question post (question - Post), and the list of posts as
  answers (answers - list of Post)
  """
  def __init__(self, title=None, question=None, answers=[], tags = [], url=None, stat='NA'):
    self.title = title
    self.question = question
    self.answers = list(answers)
    self.tags = list(tags)
    self.stat = stat
    self.url = url

  def size(self):
    cnt = 0
    if self.question != None:
      cnt = 1
    return cnt + len(self.answers)

  def write2file(self, fp):
    with open(fp, 'wb') as f:
      json.dump(self.tojson(), f)

  def tojson(self):
    json = {}
    json['title'] = self.title
    if self.question == None:
      json['question'] = None
    else:
      json['question'] = self.question.tojson()
    json['answers'] = []
    for a in self.answers:
      json['answers'].append(a.tojson())
    json['tags'] = []
    for t in self.tags:
      json['tags'].append(t)
    json['stat'] = self.stat
    json['url'] = self.url
    return json

  def fromjson(self, jt):
    self.title = jt['title']
    self.tags = list(jt['tags'])
    self.stat = jt['stat']
    self.url = jt['url']
    if jt['question'] != None:
      post = Post('', '', '', '')
      post.fromjson(jt['question'])
      self.question = post
    for a in jt['answers']:
      post = Post('', '', '', '')
      post.fromjson(a)
      self.answers.append(post)

  def __str__(self):
    if self.title == None:
      return None
    else:
      return '[' + self.stat + '] ' + self.title + ' (' + str(len(self.answers)) + ' answer)' 
