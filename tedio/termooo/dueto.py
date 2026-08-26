import random
import unicodedata
from colorama import Fore, Style, init
from unidecode import unidecode
from classico import TermoooClassico

init(autoreset=True)


class TermoooDueto(TermoooClassico):
    def __init__(self):
        super().__init__()
        self.palavrasSecretas = random.sample(self.palavras, 2)
        self.acertouPalavra1 = False
        self.acertouPalavra2 = False
        self.maxTentativas = 6
        self.tentativasPrimeiraPalavra = []
        self.tentativasSegundaPalavra = []

    def compararPalavra(self, tentativa_com_acento, secreta_com_acento):
        """Gera string formatada com Colorama para o Terminal."""
        dados = self.avaliar_palavra_dados(tentativa_com_acento, secreta_com_acento)
        resultado_str = ""
        for item in dados:
            letra = item["letra"]
            estado = item["estado"]
            if estado == "green":
                resultado_str += Fore.GREEN + letra + Style.RESET_ALL
            elif estado == "yellow":
                resultado_str += Fore.YELLOW + letra + Style.RESET_ALL
            else:
                resultado_str += Fore.LIGHTBLACK_EX + letra + Style.RESET_ALL
        return resultado_str

    def jogar(self):
        print("========== Termooo Dueto ==========")
        print("Adivinhe as duas palavras de 5 letras.")
        print(f"Você tem {self.maxTentativas} tentativas.\n")

        while len(self.tentativasPrimeiraPalavra) < self.maxTentativas:
            print(f"Tentativa {len(self.tentativasPrimeiraPalavra) + 1} de {self.maxTentativas}")
            tentativa_input = input("Digite a palavra: ").strip().upper()

            if len(tentativa_input) != 5:
                print("A palavra deve ter exatamente 5 letras.\n")
                continue

            if not self.entrada_valida(tentativa_input):
                print("Use apenas letras de A a Z, sem acentos, cedilha ou caracteres especiais.\n")
                continue

            tentativa_chave = unidecode(tentativa_input)

            if tentativa_chave not in self.word_map:
                print("Palavra inválida. Tente novamente.\n")
                continue

            tentativa_com_acento = self.word_map[tentativa_chave]

            if not self.acertouPalavra1:
                resultado1 = self.compararPalavra(tentativa_com_acento, self.palavrasSecretas[0])
            else:
                resultado1 = Fore.GREEN + self.palavrasSecretas[0] + Style.RESET_ALL

            if not self.acertouPalavra2:
                resultado2 = self.compararPalavra(tentativa_com_acento, self.palavrasSecretas[1])
            else:
                resultado2 = Fore.GREEN + self.palavrasSecretas[1] + Style.RESET_ALL

            self.tentativasPrimeiraPalavra.append(resultado1)
            self.tentativasSegundaPalavra.append(resultado2)

            print("\nTentativas:")
            for r1, r2 in zip(self.tentativasPrimeiraPalavra, self.tentativasSegundaPalavra):
                print(f"Palavra 1: {r1}   Palavra 2: {r2}")
            print()

            if tentativa_com_acento == self.palavrasSecretas[0] and not self.acertouPalavra1:
                print("Você acertou a Palavra 1!")
                self.acertouPalavra1 = True

            if tentativa_com_acento == self.palavrasSecretas[1] and not self.acertouPalavra2:
                print("Você acertou a Palavra 2!")
                self.acertouPalavra2 = True

            if self.acertouPalavra1 and self.acertouPalavra2:
                print("\nParabéns! Você acertou as duas palavras!\n")
                break
        else:
            print(f"\nVocê perdeu!")
            print(f"A palavra 1 era: {self.palavrasSecretas[0]}")
            print(f"A palavra 2 era: {self.palavrasSecretas[1]}\n")