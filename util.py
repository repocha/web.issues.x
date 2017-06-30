def dedup(lst):
  rset = set(lst)
  rlst = []
  for e in rset:
    rlst.append(e)
  return rlst

def read2lst(fpath):
  res = []
  with open(fpath) as f:
    for l in f:
      l = l.strip()
      if len(l) > 0:
        res.append(l)
  return res

def merge(flist, output):
  res = []
  for lf in flist:
    res += read2lst(lf)
  return res

def diff(l1, l2):
  res = []
  s1 = set(l1)
  for e in l2:
    if e not in s1:
      res.append(e)
  return res

def get_line_cnt(fpath):
  """
  Count #lines of the files in a given dir
  """
  return sum(1 for line in open(fpath))
