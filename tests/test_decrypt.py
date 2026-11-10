import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import decrypt


class TestDecrypt(unittest.TestCase):
    def test_lengths(self):
        self.assertEqual(len(decrypt.load_digits('451')), 1600)
        self.assertEqual(len(decrypt.load_digits('523')), 575)
        self.assertEqual(len(decrypt.pairs('451')), 764)
        self.assertEqual(len(decrypt.pairs('523')), 288)

    def test_451(self):
        t = decrypt.decrypt('451')
        self.assertTrue(t.startswith('работаберлинского'))
        self.assertIn('самыелестныеотзывы.аусвэртигесамттакжеконстатирует', t)
        self.assertIn('облегчитезаметаниеследов.', t)
        self.assertTrue(t.endswith('кмоскву'))

    def test_523(self):
        t = decrypt.decrypt('523')
        self.assertTrue(t.startswith('вашэписьмо'))
        self.assertIn('нахожуабсолютнонедопустимым.коппзаявил,чтонаркоминдэлужерэшил', t)
        self.assertIn('сдаюбродовскому', t)

    def test_reading_tables_match(self):
        key = decrypt.load_key()
        for name in ('451', '523'):
            path = os.path.join(decrypt.DATA, 'reading_%s.tsv' % name)
            with open(path, encoding='utf-8') as f:
                rows = [l.rstrip('\n').split('\t') for l in f][1:]
            self.assertEqual([r[1] for r in rows], decrypt.pairs(name))
            for r in rows:
                self.assertEqual(r[2], key.get(r[1], ''))

    def test_table_is_one_to_one(self):
        key = decrypt.load_key()
        letters = [v for v in key.values() if v not in '.,']
        self.assertEqual(len(letters), len(set(letters)))


if __name__ == '__main__':
    unittest.main()
