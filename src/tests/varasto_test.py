from contextlib import AbstractContextManager
from typing import Any
import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_negatiivinen_tilavuus(self):
        self.varasto.ota_varastosta(20)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 10)

    def test_negatiivinen_alku_saldo(self):
        self.varasto = Varasto(10, -1)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)
        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisataan_negatiivinen(self):
        self.varasto.lisaa_varastoon(-1)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_otetaan_varastosta_negatiivinen(self):
        self.varasto.lisaa_varastoon(5)
        self.varasto.ota_varastosta(-1)
        self.assertAlmostEqual(self.varasto.saldo, 5)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)
        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_lisays_liikaa(self):
        self.varasto.lisaa_varastoon(20)
        # vapaata tilaa ei pitäisi enää olla
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 0)

    def test_tyhjasta_ei_nyhjasta(self):
        saatu_maara = self.varasto.ota_varastosta(9)
        # palauttaa vain sen mitä varastossa on eli tyhjää
        self.assertAlmostEqual(saatu_maara, 0)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)
        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ei_palauta_enempaa_kuin_voi(self):
        self.varasto.lisaa_varastoon(6)

        saatu_maara = self.varasto.ota_varastosta(9)
        # palauttaa vain sen mitä varastossa on ja varastossa on tilaa nyt täydet
        self.assertAlmostEqual(saatu_maara, 6)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 10)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)
        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_palauttaa_stringin(self):
        self.assertEqual(self.__str__(), "saldo = 0, vielä tilaa 10")
