palavras = ["Abacaxi", "Girafa", "Computador", "Laranja", "Cachorro", "Laptop", "Futebol", "Oceano", "Montanha",
    "Esquilo", "Bicicleta", "Arvore", "Cultura", "Python", "Java", "Abelha", "Tecnologia", "Célula", 
    "Astronauta", "Fotografia", "Cavalo", "Mente", "Impressora", "Sol", "Lua", "Estrela", "Carro", "Avião",
    "Navio", "Cadeira", "Mesa", "Livro", "Janela", "Porta", "Televisão", "Camisa", "Calça", "Sapato", 
    "Relógio", "Cachoeira", "Floresta", "Deserto", "Rio", "Lago", "Mar", "Praia", "Pedra", "Areia", "Papel", 
    "Caneta", "Computador", "Teclado", "Celular", "Telefone", "Bateria", "Escada", "Elevador", "Janela", "Vento", 
    "Chuva", "Neve", "Sol", "Tigre", "Leão", "Cachorro", "Gato", "Elefante", "Cavalo", "Ovelha", "Fruta", "Verdura", 
    "Legume", "Manga", "Banana", "Cebola", "Alface", "Tomate", "Batata", "Feijão", "Arroz", "Macarrão", "Pizza", 
    "Sushi", "Hambúrguer", "Café", "Chá", "Água", "Refrigerante", "Pão", "Queijo", "Manteiga", "Açúcar", "Sal", 
    "Pimenta", "Alho", "Limao", "Morango", "Cabelos", "Olhos", "Boca", "Pernas", "Braços", "Coração", "Mãos", 
    "Férias", "Trabalho", "Escola", "Universidade", "Viagem"]

with open("palavras_aleatorias.txt","w") as file:
    for palavra in palavras:
        file.write(palavra + "\n")

print("Arquivo gerado com sucesso!")