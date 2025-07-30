import random
import unicodedata
from colorama import Fore, Style, init
from unidecode import unidecode

init(autoreset=True)

class TermoooDueto:
    def __init__(self):
        self.palavras, self.word_map = self.lerWordList()
        if not self.palavras:
            raise ValueError("A lista de palavras está vazia ou não pôde ser carregada.")

        self.palavrasSecretas = random.sample(self.palavras, 2)
        self.acertouPalavra1 = False
        self.acertouPalavra2 = False
        self.maxTentativas = 6
        self.tentativasPrimeiraPalavra = []
        self.tentativasSegundaPalavra = []

    def lerWordList(self):
        word_map = {}
        try:
            with open("wordlist_5letters.txt", encoding="utf-8") as wl:
                for linha in wl:
                    palavra = linha.strip().upper()
                    chave = unidecode(palavra)
                    word_map[chave] = palavra
        except FileNotFoundError:
            print("Arquivo 'wordlist_5letters.txt' não encontrado.")
            return [], {}

        return list(word_map.values()), word_map

    def remover_acentos(self,palavra):
        return ''.join(
            c for c in unicodedata.normalize('NFD', palavra)
            if unicodedata.category(c) != 'Mn'
        )

    def compararPalavra(self, tentativa_com_acento, secreta_com_acento):
        tentativa_sem_acento = self.remover_acentos(tentativa_com_acento)
        secreta_sem_acento = self.remover_acentos(secreta_com_acento)
        secreta_temp = list(secreta_sem_acento)

        resultado = [""] * len(tentativa_com_acento)

        for i in range(len(tentativa_sem_acento)):
            if tentativa_sem_acento[i] == secreta_sem_acento[i]:
                resultado[i] = Fore.GREEN + tentativa_com_acento[i] + Style.RESET_ALL
                secreta_temp[i] = None

        for i in range(len(tentativa_sem_acento)):
            if resultado[i]:
                continue
            if tentativa_sem_acento[i] in secreta_temp:
                resultado[i] = Fore.YELLOW + tentativa_com_acento[i] + Style.RESET_ALL
                secreta_temp[secreta_temp.index(tentativa_sem_acento[i])] = None
            else:
                resultado[i] = Fore.LIGHTBLACK_EX + tentativa_com_acento[i] + Style.RESET_ALL

        return ''.join(resultado)

    def jogar(self):
        print("========== Termooo Dueto ==========")
        print("Adivinhe as duas palavras de 5 letras.")
        print(f"Você tem {self.maxTentativas} tentativas.\n")

        while len(self.tentativasPrimeiraPalavra) < self.maxTentativas:
            print(f"Tentativa {len(self.tentativasPrimeiraPalavra) + 1} de {self.maxTentativas}")
            tentativa_input = input("Digite a palavra: ").strip().upper()
            tentativa_chave = unidecode(tentativa_input)

            if len(tentativa_input) != 5:
                print("A palavra deve ter exatamente 5 letras.\n")
                continue

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
