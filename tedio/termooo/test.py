import unittest
from unittest.mock import patch

from colorama import Fore, Style

from classico import TermoooClassico
from dueto import TermoooDueto


class TestTermoooClassico(unittest.TestCase):
    def test_cor_verde_quando_letra_correta_na_posicao_correta(self):
        jogo = TermoooClassico()
        jogo.palavraSecreta = "CASAL"
        resultado = jogo.compararPalavra("CASAL")
        esperado_primeira_letra = Fore.GREEN + "C" + Style.RESET_ALL
        self.assertTrue(resultado.startswith(esperado_primeira_letra))

    def test_cor_cinza_quando_letra_nao_existe(self):
        jogo = TermoooClassico()
        jogo.palavraSecreta = "CASAL"
        resultado = jogo.compararPalavra("NUVEM")
        esperado_primeira_letra = Fore.LIGHTBLACK_EX + "N" + Style.RESET_ALL
        self.assertTrue(resultado.startswith(esperado_primeira_letra))

    def test_cor_amarela_quando_letra_esta_em_posicao_errada(self):
        jogo = TermoooClassico()
        jogo.palavraSecreta = "TARDE"

        resultado = jogo.compararPalavra("DATAR")
        esperado_primeira_letra = Fore.YELLOW + "D" + Style.RESET_ALL
        self.assertTrue(resultado.startswith(esperado_primeira_letra))

    @patch("builtins.input", side_effect=["MA\u00c7\u00c3S", "MACAS"])
    def test_jogar_classico_rejeita_input_com_acento_e_cedilha(self, _input_mock):
        jogo = TermoooClassico()
        jogo.palavraSecreta = "MA\u00c7\u00c3S"
        jogo.word_map = {"MACAS": "MA\u00c7\u00c3S"}
        jogo.tentativas = []
        jogo.maxTentativas = 6

        jogo.jogar()

        self.assertEqual(len(jogo.tentativas), 1)

    @patch("builtins.input", side_effect=["MACAS"])
    def test_jogar_classico_aceita_sem_acento_e_retorna_palavra_com_acento(self, _input_mock):
        jogo = TermoooClassico()
        jogo.palavraSecreta = "MA\u00c7\u00c3S"
        jogo.word_map = {"MACAS": "MA\u00c7\u00c3S"}
        jogo.tentativas = []
        jogo.maxTentativas = 6

        jogo.jogar()

        esperado = "".join(Fore.GREEN + c + Style.RESET_ALL for c in "MA\u00c7\u00c3S")
        self.assertEqual(jogo.tentativas[0], esperado)

    @patch("builtins.input", side_effect=["CASAL"])
    def test_jogar_classico_vitoria_em_uma_tentativa(self, _input_mock):
        jogo = TermoooClassico()
        jogo.palavraSecreta = "CASAL"
        jogo.word_map = {"CASAL": "CASAL"}
        jogo.tentativas = []
        jogo.maxTentativas = 6

        jogo.jogar()

        self.assertEqual(len(jogo.tentativas), 1)


class TestTermoooDueto(unittest.TestCase):
    def test_cor_verde_no_dueto_quando_letra_correta(self):
        jogo = TermoooDueto()
        resultado = jogo.compararPalavra("CASAL", "CASAL")
        esperado_primeira_letra = Fore.GREEN + "C" + Style.RESET_ALL
        self.assertTrue(resultado.startswith(esperado_primeira_letra))

    def test_cor_amarela_no_dueto_quando_letra_esta_em_posicao_errada(self):
        jogo = TermoooDueto()
        resultado = jogo.compararPalavra("DATAR", "TARDE")
        esperado_primeira_letra = Fore.YELLOW + "D" + Style.RESET_ALL
        self.assertTrue(resultado.startswith(esperado_primeira_letra))

    def test_cor_cinza_no_dueto_quando_letra_nao_existe(self):
        jogo = TermoooDueto()
        resultado = jogo.compararPalavra("NUVEM", "CASAL")
        esperado_primeira_letra = Fore.LIGHTBLACK_EX + "N" + Style.RESET_ALL
        self.assertTrue(resultado.startswith(esperado_primeira_letra))

    @patch("builtins.input", side_effect=["MA\u00c7\u00c3S", "MACAS", "NUVEM"])
    def test_jogar_dueto_rejeita_input_com_acento_e_cedilha(self, _input_mock):
        jogo = TermoooDueto()
        jogo.palavrasSecretas = ["MA\u00c7\u00c3S", "NUVEM"]
        jogo.word_map = {"MACAS": "MA\u00c7\u00c3S", "NUVEM": "NUVEM"}
        jogo.acertouPalavra1 = False
        jogo.acertouPalavra2 = False
        jogo.tentativasPrimeiraPalavra = []
        jogo.tentativasSegundaPalavra = []
        jogo.maxTentativas = 6

        jogo.jogar()

        self.assertEqual(len(jogo.tentativasPrimeiraPalavra), 2)

    @patch("builtins.input", side_effect=["CASAL", "NUVEM"])
    def test_jogar_dueto_acerta_as_duas_palavras(self, _input_mock):
        jogo = TermoooDueto()
        jogo.palavrasSecretas = ["CASAL", "NUVEM"]
        jogo.word_map = {"CASAL": "CASAL", "NUVEM": "NUVEM"}
        jogo.acertouPalavra1 = False
        jogo.acertouPalavra2 = False
        jogo.tentativasPrimeiraPalavra = []
        jogo.tentativasSegundaPalavra = []
        jogo.maxTentativas = 6

        jogo.jogar()

        self.assertTrue(jogo.acertouPalavra1)
        self.assertTrue(jogo.acertouPalavra2)
        self.assertEqual(len(jogo.tentativasPrimeiraPalavra), 2)
        self.assertEqual(len(jogo.tentativasSegundaPalavra), 2)


if __name__ == "__main__":
    unittest.main()