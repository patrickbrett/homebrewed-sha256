from math import modf

# rotate x right by n places, assuming 32 bits
def rotr32(x, n):
  return x >> n | (x & ((1 << n) - 1)) << (32 - n)


# add mod 32
def am(x, y):
  return (x + y) % (1 << 32)


def sigma0(x):
  return rotr32(x, 7) ^ rotr32(x, 18) ^ (x >> 3)


def sigma1(x):
  return rotr32(x, 17) ^ rotr32(x, 19) ^ (x >> 10)


def usigma0(x):
  return rotr32(x, 2) ^ rotr32(x, 13) ^ rotr32(x, 22)
  

def usigma1(x):
  return rotr32(x, 6) ^ rotr32(x, 11) ^ rotr32(x, 25)


def choice(x, y, z):
  return (x & y) | (~x & z)
  

def majority(x, y, z):
  return (~(x ^ y) & x) | (~(x ^ z) & x) | (~(y ^ z) & y)

def prime_finder(n):
  primes = []
  c = 0
  x = 2
  while c < n:
    is_prime = True
    for p in primes:
      if x % p == 0:
        is_prime = False
        break
    
    if is_prime:
      primes.append(x)
      c += 1
    
    x += 1
  
  return primes


def format_k(x):
  full = x ** (1/3)
  frac, intg = modf(full)
  return int(frac * 2**32)


def format_H0(x):
  full = x ** (1/2)
  frac, intg = modf(full)
  return int(frac * 2**32)


primes = prime_finder(64)
K = [format_k(x) for x in primes]

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


def pad(x):
  padby = 512 - (len(x) % 512)
  return x + "1" + "0" * (padby - 1 - 64) + bin_to_binstr(len(x), 64)


def binf(x):
  return "{0:b}".format(x)


def hexf(x):
  return "{0:x}".format(x)


def message_to_blocks(msg):
  return [msg[m : m + 512] for m in range(0, len(msg), 512)]


def block_to_words(blk):
  return [blk[m : m + 32] for m in range(0, len(blk), 32)]


def binstr_to_bin(s):
  return int(s, 2)


def fill_sched(words):
  sched = list(map(lambda x: binstr_to_bin(x), words))

  for t in range(16, 64):
    a = sigma1(sched[t-2])
    b = sched[t-7]
    c = sigma0(sched[t-15])
    d = sched[t-16]

    w = (a + b + c + d) % (1 << 32)

    sched.append(w)
  
  return p(sched)


def p(y):
  return list(map(lambda x: bin_to_binstr(x, 32), y))


def compress(sched, H0 = None):
  if H0 is None:
    H0 = [format_H0(x) for x in primes[:8]]

  h_init = H0.copy()

  for i, word in enumerate(sched):
    a = H0[0]
    b = H0[1]
    c = H0[2]
    d = H0[3]
    e = H0[4]
    f = H0[5]
    g = H0[6]
    h = H0[7]

    W = binstr_to_bin(word)
    kk = K[i]

    T1 = (usigma1(H0[4]) + choice(H0[4], H0[5], H0[6]) + H0[7] + kk + W) % (1 << 32)
    T2 = (usigma0(H0[0]) + majority(H0[0], H0[1], H0[2])) % (1 << 32)

    # move words in state registers down one
    for i in range(7, 0, -1):
      H0[i] = H0[i-1]
    
    H0[0] = (T1 + T2) % (1 << 32)
    H0[4] = (T1 + H0[4]) % (1 << 32)

  for i in range(0, 8):
    H0[i] = (H0[i] + h_init[i]) % (1 << 32)

  return H0


def sha256(string):
  padded = pad(str_to_binstr(string))
  k = message_to_blocks(padded)

  filleds = []
  for x in k:
    words = block_to_words(x)
    filled = fill_sched(words)
    filleds.append(filled)
  
  for f in filleds:
    curr = None
    curr = compress(filled, curr)
  
  strs = p(curr)
  strs_hex = list(map(lambda x: bin_to_hexstr(binstr_to_bin(x), 2), strs))

  return "".join(strs_hex)


if __name__ == '__main__':
  res = sha256("abc")
  print(res)
