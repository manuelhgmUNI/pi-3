from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from Assembly_tradutor import Translator
from asm_to_bin import asm_bin

#def main():
with open("programas/"+"programa2.txt", "r") as arquivo:
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

tradutor = Translator()
asm = tradutor.traduzir(parcerout)

codigo_test = """
Add $r1, $r2, $r3
addi $r1, $r2, 5
lw $r1, 8($r2)
sw $r1, 8($r2)
beq $r1, $r2, 3
"""

print(asm)

resultado = asm_bin(asm)

for instrucao in resultado:
    print(instrucao, len(instrucao))


#==== ESPERANDO CONSERTO DO TRADUTRO ASM ====
#Tradutor = Translator()
#asm = Tradutor.traduzir(parcerout)

#for asm in asm:
#    print(asm)

