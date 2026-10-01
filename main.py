from lexer import Lexer

def main():
    with open("programa.txt", "r") as arquivo:
        codigo = arquivo.read()

    lexer = Lexer(codigo)

    tokens = lexer.tokenize()

    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
