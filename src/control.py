"""Control: shuffle the letter values of the table 1,000 times and score the decryptions.

The score is the mean log-probability of the letter 4-grams, from a table built on the
50,000 most frequent Russian words of the wordfreq package (pip install wordfreq).
Also scores each message with its rows read in the opposite direction.
"""
import math, random
from wordfreq import top_n_list, word_frequency
from decrypt import load_key, pairs, MESSAGES

AL = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
IDX = {c: i for i, c in enumerate(AL)}


def build():
    q = {}
    for w in top_n_list('ru', 50000):
        f = word_frequency(w, 'ru')
        t = [c for c in w.lower().replace('ё', 'е') if c in IDX]
        for i in range(len(t) - 3):
            g = ''.join(t[i:i + 4]); q[g] = q.get(g, 0.0) + f
    tot = sum(q.values())
    q = {g: math.log(v / tot) for g, v in q.items()}
    return q, min(q.values()) - 1.0


def score(tok, key, q, floor):
    t = ''.join(key[p] for p in tok if p in key and key[p] in IDX)
    return sum(q.get(t[i:i + 4], floor) for i in range(len(t) - 3)) / (len(t) - 3)


if __name__ == '__main__':
    q, floor = build()
    key = load_key()
    letters = [p for p, v in key.items() if v in IDX]
    rnd = random.Random(1921)
    for name in sorted(MESSAGES):
        tok = pairs(name)
        real = score(tok, key, q, floor)
        best, ge = -99.0, 0
        for _ in range(1000):
            vals = [key[p] for p in letters]; rnd.shuffle(vals)
            sc = score(tok, dict(zip(letters, vals)), q, floor)
            best = max(best, sc); ge += sc >= real
        w = MESSAGES[name][0] // 2
        rev = [p for i in range(0, len(tok), w) for p in tok[i:i + w][::-1]]
        print('Nr %s: real %.3f, best of 1000 shuffled keys %.3f, shuffled >= real: %d, rows read the other way %.3f'
              % (name, real, best, ge, score(rev, key, q, floor)))
