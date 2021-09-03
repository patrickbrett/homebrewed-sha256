from sha256_utils import split_arr, sigma0, sigma1, usigma0, usigma1, choice, majority, wrap32
from sha256_fmt import bin_to_binstr, bin_to_hexstr, binstr_to_bin, str_to_binstr, p
from sha256_consts import K, H0_init


def pad(x):
    padby = 512 - (len(x) % 512)
    return x + "1" + "0" * (padby - 1 - 64) + bin_to_binstr(len(x), 64)


def message_to_blocks(msg):
    return split_arr(msg, 512)


def block_to_words(blk):
    return split_arr(blk, 32)


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


def compress(sched, H0=None):
    if H0 is None:
        H0 = H0_init

    h_init = H0.copy()

    for word, kk in zip(sched, K):
        W = binstr_to_bin(word)

        T1 = wrap32((usigma1(H0[4]) + choice(H0[4], H0[5], H0[6]) + H0[7] + kk + W))
        T2 = wrap32((usigma0(H0[0]) + majority(H0[0], H0[1], H0[2])))

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
