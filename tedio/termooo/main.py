from classico import TermoooClassico
from dueto import TermoooDueto


def opcoes():
    print("Bem-vindo ao Termooo!")
    print("1 - Termooo\n2 - Dueto")

def main():
    # opcoes()

    jogarNovamente = True
    while jogarNovamente:
        opcoes()
        try:
            opcao = int(input("Escolha o modo: "))
        except ValueError:
            print("Erro: valor inválido. Esperado um número inteiro (1 ou 2).")
            return
        
        match opcao:
            case 1:
                jogo = TermoooClassico()
                jogo.jogar()
            case 2:
                jogo = TermoooDueto()
                jogo.jogar()
            case _:
                print("Modo inválido.")
                continue

        resposta = int(input("1 - SIM\n2 - NÃO\nDeseja jogar novamente?: "))
        if resposta != 1:
            jogarNovamente = False
            print("Obrigado por jogar!")
        print("\n")

if __name__ == "__main__":
    main()