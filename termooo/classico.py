import random
from colorama import Fore, Style, init
from unidecode import unidecode
import unicodedata

init(autoreset=True)

class TermoooClassico:
    def __init__(self):
        self.palavras, self.word_map = self.lerWordList()

        if not self.palavras:
            raise ValueError("A lista de palavras está vazia ou não pôde ser carregada.")

        self.chaveSecreta = random.choice(list(self.word_map.keys()))
        self.palavraSecreta = self.word_map[self.chaveSecreta]
        self.maxTentativas = 6
        self.tentativas = []

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

    def compararPalavra(self, palavraDigitada):
        palavraSemAcento = self.remover_acentos(palavraDigitada.upper())
        segredoSemAcento = self.remover_acentos(self.palavraSecreta)
        segredoTemp = list(segredoSemAcento)

        resultado = [""] * len(palavraDigitada)

        for i in range(len(palavraSemAcento)):
            if palavraSemAcento[i] == segredoSemAcento[i]:
                resultado[i] = Fore.GREEN + palavraDigitada[i] + Style.RESET_ALL
                segredoTemp[i] = None 

        for i in range(len(palavraSemAcento)):
            if resultado[i]:
                continue
            if palavraSemAcento[i] in segredoTemp:
                resultado[i] = Fore.YELLOW + palavraDigitada[i] + Style.RESET_ALL
                # Remove a letra usada para não contar duplicado
                segredoTemp[segredoTemp.index(palavraSemAcento[i])] = None
            else:
                # Letra não está na palavra (cinza)
                resultado[i] = Fore.LIGHTBLACK_EX + palavraDigitada[i] + Style.RESET_ALL

        return ''.join(resultado)

    def jogar(self):
        print("========== Termooo Clássico ==========")
        print(f"Adivinhe a palavra de {len(self.palavraSecreta)} letras. Você tem {self.maxTentativas} tentativas.\n")

        while len(self.tentativas) < self.maxTentativas:
            print(f"Tentativa {len(self.tentativas)+1} de {self.maxTentativas}")
            palavraDigitada = input("Digite a palavra: ").strip().upper()
            palavraChave = unidecode(palavraDigitada)

            if len(palavraDigitada) != len(self.palavraSecreta):
                print(f"A palavra deve ter exatamente {len(self.palavraSecreta)} letras.\n")
                continue

            if palavraChave not in self.word_map:
                print("Palavra inválida. Tente novamente.\n")
                continue

            palavraComAcento = self.word_map[palavraChave]
            resultado = self.compararPalavra(palavraComAcento)
            self.tentativas.append(resultado)

            print("\nTentativas até agora:")
            for linha in self.tentativas:
                print(linha)
            print()

            if palavraComAcento == self.palavraSecreta:
                print("Parabéns! Você acertou a palavra!\n")
                break
        else:
            print(f"Você perdeu! A palavra era: {self.palavraSecreta}\n")
