import random
import requests
from colorama import Fore, Style, init

init(autoreset=True)

class TermoooClassico:
    def __init__(self):
        self.palavras = self.lerPalavrasOnline()
        
        if not self.palavras:
            raise ValueError("A lista de palavras está vazia ou não pôde ser carregada.")

        self.palavraSecreta = random.choice(self.palavras)
        self.maxTentativas = 6
        self.tentativas = []

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

    def compararPalavra(self, palavraDigitada):
        resultado = []
        palavraSecreta_temp = list(self.palavraSecreta)

        for i in range(len(palavraDigitada)):
            if palavraDigitada[i] == self.palavraSecreta[i].upper():
                resultado.append(Fore.GREEN + palavraDigitada[i] + Style.RESET_ALL)
                palavraSecreta_temp[i] = None 
            else:
                resultado.append(None)

        for i in range(len(palavraDigitada)):
            if resultado[i] is not None:
                continue
            if palavraDigitada[i] in palavraSecreta_temp:
                resultado[i] = Fore.YELLOW + palavraDigitada[i] + Style.RESET_ALL
                palavraSecreta_temp[palavraSecreta_temp.index(palavraDigitada[i])] = None
            else:
                resultado[i] = Fore.LIGHTBLACK_EX + palavraDigitada[i] + Style.RESET_ALL

        return "".join(resultado)

    def jogar(self):
        print("==========Termooo genérico==========")
        print(f"Adivinhe a palavra de {len(self.palavraSecreta)} letras. Você tem {self.maxTentativas} tentativas.\n")

        while len(self.tentativas) < self.maxTentativas:
            print(f"Tentativa {len(self.tentativas)+1} de {self.maxTentativas}")
            palavraDigitada = input("Digite a palavra: ").strip().upper()

            if len(palavraDigitada) != len(self.palavraSecreta):
                print(f"A palavra deve ter exatamente {len(self.palavraSecreta)} letras.\n")
                continue

            if palavraDigitada not in self.palavras:
                print("Palavra inválida. Tente novamente.\n")
                continue

            resultado = self.compararPalavra(palavraDigitada)
            self.tentativas.append(resultado)

            print("\nTentativas até agora:")
            for linha in self.tentativas:
                print(linha)
            print()

            if palavraDigitada == self.palavraSecreta:
                print("Parabéns! Você acertou a palavra!\n")
                break
        else:
            print(f"Você perdeu! A palavra era: {self.palavraSecreta}\n")