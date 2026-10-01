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