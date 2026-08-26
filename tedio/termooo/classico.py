import random
import unicodedata
from colorama import Fore, Style, init
from unidecode import unidecode

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

    def remover_acentos(self, palavra):
        return ''.join(
            c for c in unicodedata.normalize('NFD', palavra)
            if unicodedata.category(c) != 'Mn'
        )

    def entrada_valida(self, palavra):
        return palavra.isalpha() and palavra.isascii()

    def avaliar_palavra_dados(self, palavraDigitada, secretaTarget=None):
        """
        Retorna uma lista de dicts para o frontend (Streamlit).
        Exemplo: [{"letra": "A", "estado": "green"}, ...]
        Estados possíveis: "green", "yellow", "gray"
        """
        target = secretaTarget if secretaTarget else self.palavraSecreta
        palavraSemAcento = self.remover_acentos(palavraDigitada.upper())
        segredoSemAcento = self.remover_acentos(target)
        segredoTemp = list(segredoSemAcento)

        resultado = [{"letra": palavraDigitada[i].upper(), "estado": "gray"} for i in range(len(palavraDigitada))]

        # 1ª passada: Verdes (letra certa no lugar certo)
        for i in range(len(palavraSemAcento)):
            if palavraSemAcento[i] == segredoSemAcento[i]:
                resultado[i]["estado"] = "green"
                segredoTemp[i] = None

        # 2ª passada: Amarelos (letra certa no lugar errado)
        for i in range(len(palavraSemAcento)):
            if resultado[i]["estado"] == "green":
                continue
            if palavraSemAcento[i] in segredoTemp:
                resultado[i]["estado"] = "yellow"
                segredoTemp[segredoTemp.index(palavraSemAcento[i])] = None

        return resultado

    def compararPalavra(self, palavraDigitada):
        """Gera string formatada com Colorama para o Terminal."""
        dados = self.avaliar_palavra_dados(palavraDigitada)
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
        print("========== Termooo Clássico ==========")
        print(f"Adivinhe a palavra de {len(self.palavraSecreta)} letras. Você tem {self.maxTentativas} tentativas.\n")

        while len(self.tentativas) < self.maxTentativas:
            print(f"Tentativa {len(self.tentativas)+1} de {self.maxTentativas}")
            palavraDigitada = input("Digite a palavra: ").strip().upper()

            if len(palavraDigitada) != len(self.palavraSecreta):
                print(f"A palavra deve ter exatamente {len(self.palavraSecreta)} letras.\n")
                continue

            if not self.entrada_valida(palavraDigitada):
                print("Use apenas letras de A a Z, sem acentos, cedilha ou caracteres especiais.\n")
                continue

            palavraChave = unidecode(palavraDigitada)

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