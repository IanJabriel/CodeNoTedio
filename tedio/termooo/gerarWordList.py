import requests

def gerarWordList():
        urls = [ 
            "https://raw.githubusercontent.com/fserb/pt-br/refs/heads/master/verbos",
            "https://raw.githubusercontent.com/fserb/pt-br/refs/heads/master/conjuga%C3%A7%C3%B5es",
            "https://raw.githubusercontent.com/fserb/pt-br/refs/heads/master/dicio",
            "https://raw.githubusercontent.com/fserb/pt-br/refs/heads/master/palavras",
        ]

        palavras_set = set()

        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                for linha in response.text.splitlines():
                    palavra = linha.strip()
                    if len(palavra) == 5 and palavra.isalpha():
                        palavras_set.add(palavra.upper())
            except Exception as e:
                print(f"Erro ao baixa {url}")

        with open("wordlist_5letters.txt","w",encoding="utf-8") as wl:
            for palavra in sorted(palavras_set):
                wl.write(palavra + "\n")

gerarWordList()