import random

class JogoForca:
    def __init__(self,arquivo):
        self.palavras = self.lerPalavrasArquivo(arquivo)
        
        if not self.palavras:
            raise ValueError("O arquivo de palavras está vazio ou não existe.")

        self.palavraSecreta = random.choice(self.palavras)
        self.tentativas = 0
        self.maxTentativas = 6
        self.letraErrada = []
        self.letraTentada = []
        self.laytout = ["_"] * len(self.palavraSecreta)

    def lerPalavrasArquivo(self,arquivo):
        try:
            with open(arquivo,"r") as arq:
                palavras = [linha.strip() for linha in arq.readlines() if linha.strip()]
            
            return palavras
        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado!")
            return []

    def exibirPalavra(self):
        print("".join(self.laytout))

    def verificarTentativa(self, letra):
        if letra in self.letraTentada:
            print("Você já tentou essa letra. Tente uma letra diferente.")
            return False
        self.letraTentada.append(letra)
        
        if letra.lower() in self.palavraSecreta.lower():
            for i in range(len(self.palavraSecreta)):
                if self.palavraSecreta[i].lower() == letra.lower():
                    self.laytout[i] = letra
            return True
        else:
            self.letraErrada.append(letra)
            self.tentativas += 1
            return False

    def jogoTerminado(self):
        return self.tentativas >= self.maxTentativas or "_" not in self.laytout

    def resultado(self):
        if "_" not in self.laytout:
            print(f"Parabéns! Você acertou a palavra: {self.palavraSecreta}")
        else:
            print(f"Você perdeu! A palavra secreta era: {self.palavraSecreta}")   

    def jogar(self):
        print("Bem-vindo ao jogo da Forca!")
        
        while not self.jogoTerminado():
            self.exibirPalavra()
            letra = input("Digite uma letra: ").upper()

            if len(letra) != 1 or not letra.isalpha():
                print("Por favor, digite apenas uma letra válida!")
                continue 

            if self.verificarTentativa(letra):
                print(f"Você acertou a letra '{letra}'!")
            else:
                print(f"Letras erradas: {', '.join(self.letraErrada)}")
            
            print(f"Tentativas restantes: {self.maxTentativas - self.tentativas}\n")

        print("-------------------------------------------------------")    
        self.resultado()
        print("-------------------------------------------------------")    

if __name__ == "__main__":
    try:
        jogo = JogoForca(arquivo="palavras_aleatorias.txt")
        jogo.jogar()
    except ValueError as e:
        print(e)