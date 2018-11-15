import unittest

from paprika.system.Ora import Ora

class TestBase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_decode(self):
        s = ''
        decode = Ora.decode(s, 'COM', 'Organisatie')
        self.assertEqual(decode, None, 'expected None was ' + str(decode))

        s = 'COM'
        decode = Ora.decode(s, 'COM', 'Organisatie')
        self.assertEqual(decode, 'Organisatie', 'expected Organisatie was ' + str(decode))

        s = 'PER'
        decode = Ora.decode(s, 'COM', 'Organisatie', 'Other')
        self.assertEqual(decode, 'Other', 'expected Other was ' + str(decode))

    def test_nvl(self):
        s = ''
        self.assertEqual(Ora.nvl(s, 'PER'), 'PER', 'expected PER was ' + Ora.nvl(s, 'PER'))

    def test_nnvl_decode(self):
        print Ora.nnvl_decode('', '1', '', '2', '3')

    def test_fsdate(self):
        datum_sleuteloverdracht = None
        gewenste_ingangsdatum_contract = '30102017'
        result = Ora.fsdate(Ora.nvl2(datum_sleuteloverdracht, datum_sleuteloverdracht, Ora.fsdate(gewenste_ingangsdatum_contract,'%d%m%Y','%d-%m-%Y')),'%d-%m-%Y', '%Y-%m-%d')
        #Ora.fsdate(Ora.nvl2(datum_sleuteloverdracht, datum_sleuteloverdracht, Ora.fsdate(gewenste_ingangsdatum_contract,'%d%m%Y', '%d-%m-%Y'), '%d-%m-%Y', '%Y-%m-%d'))
        self.assertEqual(result, '2017-10-30', 'expected 2017-10-30 was ' + result)

    def test_concat(self):
        avond_net_nummer = Ora.nvl(None, '')
        avond_abonnee_nummer = Ora.nvl('0612345678', '')
        avond_nummer = avond_net_nummer + avond_abonnee_nummer
        if avond_nummer:
            print Ora.decode(avond_nummer.startswith('06'), True, 'Mobiel', 'Prive')
            print avond_nummer


if __name__ == '__main__':
    unittest.main()
