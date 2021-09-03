
def binstr_to_bin(s):
  return int(s, 2)



def bin_to_binstr(x, l):
  x = binf(x)
  if len(x) < l:
    x = "0" * (l - len(x)) + x
  return x


def bin_to_hexstr(x, l):
  x = hexf(x)
  if len(x) < l:
    x = "0" * (l - len(x)) + x
  return x


def str_to_binstr(s):
  binstr = ""
  for char in s:
    binstr += bin_to_binstr(ord(char), 8)
  return binstr


def binf(x):
  return "{0:b}".format(x)


def hexf(x):
  return "{0:x}".format(x)


def p(y):
  return list(map(lambda x: bin_to_binstr(x, 32), y))
