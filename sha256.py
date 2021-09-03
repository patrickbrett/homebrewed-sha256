from math import modf

# Utils

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
  return ((x ^ y) & z) | ((x ^ z) & y) | ((y ^ z) & x)


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

primes = prime_finder(64)
K = [format_k(x) for x in primes]

print(K)

def bin_to_binstr(x, l):
  x = binf(x)
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

print(pad(str_to_binstr("abc")))

# print("{0:b}".format(rotr32(0b10101010101010101010101010101011, 7)))
# print("{0:b}".format(sigma0(0b00000000000000000011111111111111)))
# print("{0:b}".format(choice(0b00000000111111110000000011111111, 0b00000000000000001111111111111111, 0b11111111111111110000000000000000)))
# print("{0:b}".format(majority(0b00000000111111110000000011111111, 0b00000000000000001111111111111111, 0b11111111111111110000000000000000)))

