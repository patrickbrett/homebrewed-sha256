def binstr_to_bin(s):
    return int(s, 2)


def pad_str(x, l, fmt):
    x = fmt(x)
    if len(x) < l:
        x = "0" * (l - len(x)) + x
    return x


def bin_to_binstr(x, l):
    return pad_str(x, l, binf)


def bin_to_hexstr(x, l):
    return pad_str(x, l, hexf)


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
