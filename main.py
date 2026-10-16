from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer

#def main():
with open("programas/"+"programaerro1.txt", "r") as arquivo:
    codigo = arquivo.read()

print("\nchamando lexer...")

lexer = Lexer(codigo)

tokens = lexer.tokenize()

for token in tokens:
    print(token)

#print("\nchamando Parser...")

print("\ninicializando Parser...")
parser = Parser(tokens)

print("executando Parser...")
parcerout = parser.parse()

print("imprimindo resultados...")
print("Program "+parcerout.nome)
Po = parcerout.comandos
for Po in Po:
    print(Po)

print("\niniciando analizador...")
fiscal = SemanticAnalyzer()

print("executando analize semantica...")
fiscal.analisar(parcerout)

print("analize concluida!")

# print(parcerout[0]+" "+parcerout[1])
#for parcerout[2] in parcerout[2]:
   #print(parcerout[2])

#print(type(parcerout[2][0]))   



#if __name__ == "__main__":
#    main()
