import unicodedata

a = input("Digite sua palavra: ")

def remove_acento(a):
    return ''.join(x for x in unicodedata.normalize("NFD",a)if unicodedata.category(x) != 'Mn')

print(remove_acento(a))