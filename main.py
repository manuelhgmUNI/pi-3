
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from Assembly_tradutor import Translator
from asm_to_bin import asm_bin

# Leitura do programa DSL
with open("programas/" + "programa2.txt", "r") as arquivo:
    codigo = arquivo.read()

print("\nChamando Lexer...")

lexer = Lexer(codigo)
tokens = lexer.tokenize()

for token in tokens:
    print(token)

print("\nInicializando Parser...")
parser = Parser(tokens)

print("Executando Parser...")
parcerout = parser.parse()

print("\nImprimindo resultados...")
print("Program " + parcerout.nome)

Po = parcerout.comandos
for Po in Po:
    print(Po)

print("\nIniciando analisador...")
fiscal = SemanticAnalyzer()

print("Executando análise semântica...")
fiscal.analisar(parcerout)

print("Análise concluída!")

# Tradução da DSL para Assembly MiniMIPS
print("\nIniciando tradução para Assembly MiniMIPS...")

tradutor = Translator()
asm = tradutor.traduzir(parcerout)

print("\nCódigo Assembly MiniMIPS:")
print(asm)

# Conversão do Assembly para código binário
print("\nConvertendo Assembly para código binário...")

resultado = asm_bin(asm)

print("\nCódigo binário:")
for instrucao in resultado:
    print(instrucao, len(instrucao))

   #print(parcerout[2])

#print(type(parcerout[2][0]))   



#if __name__ == "__main__":
#    main()
