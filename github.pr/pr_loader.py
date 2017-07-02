import os
import json
import utils

def dump_prs(dirp, repo, fp):
  res = []
  for fn in os.listdir(dirp):
    with open(os.path.join(dirp, fn)) as f:
      prurl = utils.gen_prurl(utils.reponame2repourl(repo), fn)
      res.append((prurl, f.read()))
  with open(fp, 'w') as f:
     json.dump(res, f)

def load_prs(fp):
  with open(fp) as f:
     return json.load(f)

def batch_dump(src_dir, dest_dir):
  """this only works with the current dir hierarchy
  """
  for repo in os.listdir(src_dir):
    dump_prs(os.path.join(src_dir, repo), repo, os.path.join(dest_dir, repo))

def loadall(dirp):
  """this only works with the current dir hierarchy
  """
  dumps = {}
  for repo in os.listdir(dirp):
    dumps[urlrepo] = load_prs(os.path.join(dirp, repo))
  return dumps

#if __name__ == "__main__":
#  ROOT = 'tests'
#  DEST = 'tests_aggr'
#  batch_dump(ROOT, DEST)

