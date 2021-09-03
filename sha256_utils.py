
from sha256_fmt import bin_to_binstr
from math import modf

"""
rotate x right by n places, assuming 32 bits
"""
def rotr32(x, n):
    return x >> n | (x & ((1 << n) - 1)) << (32 - n)


def sigma0(x):
    return rotr32(x, 7) ^ rotr32(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotr32(x, 17) ^ rotr32(x, 19) ^ (x >> 10)


def usigma0(x):
    return rotr32(x, 2) ^ rotr32(x, 13) ^ rotr32(x, 22)


def usigma1(x):
    return rotr32(x, 6) ^ rotr32(x, 11) ^ rotr32(x, 25)


# if the x bit is 1, return the y bit, otherwise return the z bit
def choice(x, y, z):
    return (x & y) | (~x & z)


# majority rules for each bit out of the bits supplied by x, y and z
def majority(x, y, z):
    return (~(x ^ y) & x) | (~(x ^ z) & x) | (~(y ^ z) & y)


# naive prime search
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


def format_const(x, pwr):
    full = x ** pwr
    frac, intg = modf(full)
    return int(frac * 2**32)


def format_k(x):
    return format_const(x, 1/3)


def format_H0(x):
    return format_const(x, 1/2)


def split_arr(arr, block_size):
    return [arr[m: m + block_size] for m in range(0, len(arr), block_size)]


def wrap32(x):
    return x % (1 << 32)
