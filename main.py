from lexer import Lexer
from parser import Parser

#def main():
with open("programas/"+"programa2.txt", "r") as arquivo:
    codigo = arquivo.read()

print("\nchamando lexer...")

lexer = Lexer(codigo)

tokens = lexer.tokenize()

for token in tokens:
    print(token)

#print("\nchamando Parser...")

print("inicializando Parser...")
parser = Parser(tokens)

print("executando Parser...")
parcerout = parser.parse()

print("imprimindo resultados...")
print("Program "+parcerout.nome)
Po = parcerout.comandos
for Po in Po:
    print(Po)

# print(parcerout[0]+" "+parcerout[1])
#for parcerout[2] in parcerout[2]:
   #print(parcerout[2])

#print(type(parcerout[2][0]))   



#if __name__ == "__main__":
#    main()
