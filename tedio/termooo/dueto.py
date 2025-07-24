import random
import requests
from colorama import Fore, Style, init

init(autoreset=True)

class TermoooDueto:
    def __init__(self):
        self.palavras = self.lerPalavrasOnline()
        if not self.palavras:
            raise ValueError("A lista de palavras está vazia ou não pôde ser carregada.")

        self.palavrasSecretas = random.sample(self.palavras, 2)
        self.acertouPalavra1 = False
        self.acertouPalavra2 = False
        self.maxTentativas = 6
        self.tentativasPrimeiraPalavra = []
        self.tentativasSegundaPalavra = []

    def lerPalavrasOnline(self):
        url = "https://gist.githubusercontent.com/vncsmnl/25e7c165da276405af8ca4e1c8e17806/raw/bd238615c9089721a16418289589961490d0cf65/wordlist"
        try:
            response = requests.get(url)
            response.raise_for_status()
            palavras = response.text.splitlines()
            return [p.strip().upper() for p in palavras if len(p.strip()) == 5]
        except requests.RequestException as e:
            print("Erro ao acessar a wordlist online:", e)
            return []

    def compararPalavra(self, tentativa, palavraSecreta):
        resultado = []
        palavra_temp = list(palavraSecreta)

        for i in range(len(tentativa)):
            if tentativa[i] == palavraSecreta[i]:
                resultado.append(Fore.GREEN + tentativa[i] + Style.RESET_ALL)
                palavra_temp[i] = None
            else:
                resultado.append(None)

        for i in range(len(tentativa)):
            if resultado[i] is not None:
                continue
            if tentativa[i] in palavra_temp:
                resultado[i] = Fore.YELLOW + tentativa[i] + Style.RESET_ALL
                palavra_temp[palavra_temp.index(tentativa[i])] = None
            else:
                resultado[i] = Fore.LIGHTBLACK_EX + tentativa[i] + Style.RESET_ALL

        return "".join(resultado)

    def jogar(self):
        print("========== Termooo Dueto ==========")
        print("Adivinhe as duas palavras de 5 letras.")
        print(f"Você tem {self.maxTentativas} tentativas.\n")

        while len(self.tentativasPrimeiraPalavra) < self.maxTentativas:
            print(f"Tentativa {len(self.tentativasPrimeiraPalavra) + 1} de {self.maxTentativas}")
            tentativa = input("Digite a palavra: ").strip().upper()

            if len(tentativa) != len(self.palavrasSecretas[0]):
                print(f"A palavra deve ter exatamente {len(self.palavrasSecretas[0])} letras.\n")
                continue

            if tentativa not in self.palavras:
                print("Palavra inválida. Tente novamente.\n")
                continue

            if not self.acertouPalavra1:
                resultado1 = self.compararPalavra(tentativa, self.palavrasSecretas[0])
            else:
                resultado1 = Fore.GREEN + self.palavrasSecretas[0] + Style.RESET_ALL

            if not self.acertouPalavra2:
                resultado2 = self.compararPalavra(tentativa, self.palavrasSecretas[1])
            else:
                resultado2 = Fore.GREEN + self.palavrasSecretas[1] + Style.RESET_ALL

            self.tentativasPrimeiraPalavra.append(resultado1)
            self.tentativasSegundaPalavra.append(resultado2)

            print("\nTentativas:")
            for r1, r2 in zip(self.tentativasPrimeiraPalavra, self.tentativasSegundaPalavra):
                print(f"Palavra 1: {r1}   Palavra 2: {r2}")
            print()

            if tentativa == self.palavrasSecretas[0] and not self.acertouPalavra1:
                print("Você acertou a Palavra 1!")
                self.acertouPalavra1 = True

            if tentativa == self.palavrasSecretas[1] and not self.acertouPalavra2:
                print("Você acertou a Palavra 2!")
                self.acertouPalavra2 = True

            if self.acertouPalavra1 and self.acertouPalavra2:
                print("\nParabéns! Você acertou as duas palavras!\n")
                break
        else:
            print(f"\nVocê perdeu!")
            print(f"A palavra 1 era: {self.palavrasSecretas[0]}")
            print(f"A palavra 2 era: {self.palavrasSecretas[1]}\n")