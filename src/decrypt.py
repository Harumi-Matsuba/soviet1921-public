"""Decrypt Funkspruch Nr 451 and Nr 523 (NARA M316 roll 43, frames 0427-0428 and 0432).

System: each letter is a pair of digits from a 5 x 6 table (first digit 6,7,8,9,0; second digit 0-5).
The pairs are written row by row into a square whose side N is spelled out before the groups
(SOROK = 40, DWADZAT TCHETYRE = 24), N/2 pairs to a row, and the square is sent column by column.

Nr 451: digit columns alternate first digit / second digit; the rows are read right to left.
Nr 523: digit columns alternate second digit / first digit; the rows are read left to right.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
MESSAGES = {'451': (40, False), '523': (24, True)}   # side of the square, mirrored layout


def load_digits(name):
    with open(os.path.join(DATA, 'ciphertext_%s.txt' % name), encoding='utf-8') as f:
        return ''.join(c for line in f if not line.startswith('#') for c in line if c.isdigit())


def load_key():
    key = {}
    with open(os.path.join(DATA, 'key.tsv'), encoding='utf-8') as f:
        next(f)
        for line in f:
            pair, value, note = line.rstrip('\n').split('\t')
            if value and 'not counted as read' not in note:
                key[pair] = value
    return key


def pairs(name):
    """The pairs of one message in reading order, named first digit (6,7,8,9,0) + second digit."""
    n, mirrored = MESSAGES[name]
    s = load_digits(name)
    s = s + '?' * (n * n - len(s))
    cols = [s[i:i + n] for i in range(0, n * n, n)]
    out = []
    for r in range(n):
        if mirrored:
            row = [cols[2 * j + 1][r] + cols[2 * j][r] for j in range(n // 2)]
        else:
            row = [cols[2 * j][r] + cols[2 * j + 1][r] for j in range(n // 2)][::-1]
        out.extend(row)
    while out and out[-1] == '00':
        out.pop()
    return out


def decrypt(name, key=None):
    key = key or load_key()
    return ''.join(key.get(p, '[%s]' % p) for p in pairs(name))


if __name__ == '__main__':
    for name in sys.argv[1:] or sorted(MESSAGES):
        print('Nr', name)
        print(decrypt(name))
        print()
