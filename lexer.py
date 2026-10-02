class Token:
    def __init__(self, tipo, valor, linha, coluna):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor!r}, linha={self.linha}, coluna={self.coluna})"

class Lexer:
    PALAVRAS_RESERVADAS = {
        "program": "PROGRAM",
        "if": "IF",
        "else": "ELSE",
        "while": "WHILE",
        "repeat": "REPEAT",

        "MvUp": "MV_UP",
        "MvDown": "MV_DOWN",
        "MvLeft": "MV_LEFT",
        "MvRight": "MV_RIGHT",

        "IfWallUp": "IF_WALL_UP",
        "IfWallDown": "IF_WALL_DOWN",
        "IfWallLeft": "IF_WALL_LEFT",
        "IfWallRight": "IF_WALL_RIGHT",
        "PackSee": "PACK_SEE",

        "PackCat": "PACK_CAT",
        "PackDrop": "PACK_DROP",

        "true": "TRUE",
        "false": "FALSE"
    }

    def __init__(self, codigo):
        self.codigo = codigo
        self.posicao = 0
        self.linha = 1
        self.coluna = 1

    def avancar(self):
        char = self.codigo[self.posicao]
        self.posicao += 1

        if char == "\n":
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1

        return char

    def peek(self):
        if self.posicao >= len(self.codigo):
            return None

        return self.codigo[self.posicao]

    def tokenize(self):
        tokens = []

        while self.posicao < len(self.codigo):
            char = self.peek()

            # Espaços
            if char.isspace():
                self.avancar()
                continue

            linha = self.linha
            coluna = self.coluna

            # Identificadores / palavras reservadas
            if char.isalpha() or char == "_":
                palavra = self.ler_identificador()

                if palavra in self.PALAVRAS_RESERVADAS:
                    tipo = self.PALAVRAS_RESERVADAS[palavra]
                else:
                    tipo = "IDENTIFIER"

                tokens.append(Token(tipo, palavra, linha, coluna))

            # Numeros
            elif char.isdigit():
                numero = self.ler_numero()

                tokens.append(Token("NUMBER", numero, linha, coluna))

            # {
            elif char == "{":
                self.avancar()
                tokens.append(Token("LBRACE", "{", linha, coluna))

            # }
            elif char == "}":
                self.avancar()
                tokens.append(Token("RBRACE", "}", linha, coluna))

            # ==
            elif char == "=":      # >==
                self.avancar()     # =>=

                if self.peek() == "=":
                    self.avancar() # ==>

                    tokens.append(Token("EQUAL", "==", linha, coluna))
                else:
                    raise SyntaxError(f"Esperado '=' na linha {linha}, coluna {coluna + 1}")

            # !=
            elif char == "!":      # >!=
                self.avancar()     # !>=

                if self.peek() == "=":
                    self.avancar() # !=>

                    tokens.append(Token("NOT_EQUAL", "!=", linha, coluna))
                else:
                    raise SyntaxError(f"Esperado '=' após '!' na linha {linha}, coluna {coluna}")

            else:
                raise SyntaxError(f"Caractere inválido '{char}' " f"na linha {linha}, coluna {coluna}")

        tokens.append(Token("EOF", "", self.linha, self.coluna))

        return tokens

    def ler_identificador(self):
        resultado = ""

        while self.peek() is not None:
            char = self.peek()

            if char.isalnum() or char == "_":
                resultado += self.avancar()
            else:
                break

        return resultado

    def ler_numero(self):
        resultado = ""

        while self.peek() is not None and self.peek().isdigit():
            resultado += self.avancar()

        return int(resultado)

