class Romano():
    def __init__(self):
        self.romanos = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }

        self.nao_repetiveis = {"V", "L", "D"}
        self.max_repeticao = 3

        self.subtracoes = {
            "I": {"V", "X"}, 
            "X": {"L", "C"},
            "C": {"D", "M"}
        }

    def validar_romanos(self, romano: str) -> bool:
        anterior = ""
        repeticoes = 1

        for i in range(len(romano)):
            atual = romano[i]

            if atual not in self.romanos:
                print("Símbolo inválido")
                return False

            if atual == anterior:
                repeticoes += 1

                if atual in self.nao_repetiveis:
                    print(f"Símbolo {atual} não pode ser repetido")
                    return False

                if repeticoes > self.max_repeticao:
                    print(f"Símbolo {atual} repetido mais de {self.max_repeticao} vezes.")
                    return False

            else:
                repeticoes = 1

            if i + 1 < len(romano):
                proximo = romano[i + 1]
                if self.romanos[atual] < self.romanos[proximo]:
                    if atual not in self.subtracoes or proximo not in self.subtracoes[atual]:
                        print(f"Subtração inválida: {atual} antes de {proximo}")
                        return False

            anterior = atual

        return True

    def inteiro_para_romano(self, numero: int) -> str:
        if numero <= 0 or numero > 3999:
            raise ValueError("Número fora do intervalo permitido (1 a 3999)")

        resultado = ""
        valores = list(self.romanos.items())
        valores.sort(key=lambda x: x[1], reverse=True)

        i = 0
        while numero > 0 and i < len(valores):
            simbolo, valor = valores[i]

            if numero >= valor:
                resultado += simbolo
                numero -= valor
            else:
                for menor, val_menor in self.romanos.items():
                    if menor in self.subtracoes and simbolo in self.subtracoes[menor]:
                        if numero >= valor - val_menor:
                            resultado += menor + simbolo
                            numero -= (valor - val_menor)
                            break
                else:
                    i += 1

        if not self.validar_romanos(resultado):
            raise ValueError(f"Erro: a conversão gerou um número romano inválido: {resultado}")

        return resultado

def main():
    romano = Romano()

    print("Converter 1994:", romano.inteiro_para_romano(1994))  # MCMXCIV
    print("Converter 944:", romano.inteiro_para_romano(944))    # CMXLIV
    print("Converter 4:", romano.inteiro_para_romano(4))        # IV
    print("Converter 2004:", romano.inteiro_para_romano(2004))        # IV

if __name__ == "__main__":
    main()