from sha256_utils import prime_finder, format_k, format_H0

primes = prime_finder(64)
K = [format_k(x) for x in primes]
H0_init = [format_H0(x) for x in primes[:8]]
