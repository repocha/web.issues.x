def reponame2repourl(name):
  return 'https://github.com/' + name.replace('.', '/', 1)

def gen_prurl(repourl, prid):
  return repourl + '/pull/' + prid  
