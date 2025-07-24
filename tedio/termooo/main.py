from classico import TermoooClassico
from dueto import TermoooDueto


def main():
    print("Bem-vindo ao Termooo!")
    print("1 - Termooo\n2 - Dueto")

    try:
        opcao = int(input("Escolha o modo (1 ou 2): "))
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

if __name__ == "__main__":
    main()
