from lexer import Lexer
from Parser import Parser

def main():
    with open("programa.txt", "r") as arquivo:
        codigo = arquivo.read()

    print("\nchamando lexer...")

    lexer = Lexer(codigo)

    tokens = lexer.tokenize()

    for token in tokens:
        print(token)

    print("\nchamando Parser...")

    parser = parser(tokens)

    parcerout = parser.programa()

    for parcerout in parcerout:
        print(parcerout)
    



if __name__ == "__main__":
    main()
