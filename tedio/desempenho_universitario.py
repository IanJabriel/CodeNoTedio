import csv

def leitor_csv(arquivo):
    with open(arquivo, newline="", encoding="utf-8") as csvfile:
        leitor = csv.DictReader(csvfile)
        for linha in leitor:
            yield linha

def extrair_notas(arquivo):
    for linha in leitor_csv(arquivo):
        notas = float(linha["Média"].split(",")[0])
        yield notas

def calcular_media_nota(arquivo):
    notas = 0
    qtd_nota = 0
    for nota in extrair_notas(arquivo):
        notas += nota
        qtd_nota += 1
    media = notas / qtd_nota
    return media

def calcular_media_frequencia(arquivo):
    frequencias = 0
    qtd_frequencia = 0
    for linha in leitor_csv(arquivo):
        frequencia = float(linha["Frequência"].split(",")[0])
        frequencias += frequencia
        qtd_frequencia += 1
    media = frequencias / qtd_frequencia
    return media

def main():
    arquivo = "arquivo.csv"
    media_nota = calcular_media_nota(arquivo)
    media_frequencia = calcular_media_frequencia(arquivo)

    print(f"Minha média de notas da faculdade é: {media_nota:.2f}")
    print(f"Minha média de frequência da faculdade é: {media_frequencia:.2f}%")

if __name__ == "__main__":
    main()