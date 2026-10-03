class Parser:
    from lexer import Token

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def atual(self):
        return self.tokens[self.posicao]

    def avancar(self):
        token = self.atual()
        self.posicao += 1
        return token

    def esperar(self, tipo):
        token = self.atual()
        if token.tipo != tipo:
            raise SyntaxError(
                f"Esperado {tipo}, "
                f"mas encontrado {token.tipo} "
                f"({token.valor!r}) "
                f"na linha {token.linha}, "
                f"coluna {token.coluna}"
            )
        return self.avancar()


    def parse(self):
        programa = self.programa()
        self.esperar("EOF")
        return programa

    # Programa

    def programa(self):
        resultado = []

        self.esperar("PROGRAM")
        nome = self.esperar("IDENTIFIER")
        self.esperar("LBRACE")

        comandos = []
        while self.atual().tipo != "RBRACE":
            if self.atual().tipo == "EOF":
                token = self.atual()
                raise SyntaxError(
                    f"Esperado '}}' na linha "
                    f"{token.linha}, coluna "
                    f"{token.coluna}"
                )
            comandos.append(self.comando())
        self.esperar("RBRACE")

        resultado.append("PROGRAM")
        resultado.append(nome.valor)
        resultado.append(comandos)
        return  resultado
        #{
        #    "tipo": "PROGRAM",
        #    "nome": nome.valor,
        #    "comandos": comandos
        #}

    # Comandos

    def comando(self):

        tipo = self.atual().tipo
        if tipo in {
            "MV_UP",
            "MV_DOWN",
            "MV_LEFT",
            "MV_RIGHT"
        }:
            return self.movimento()
        
        elif tipo == "PACK_CAT":
            return self.pack_cat()

        elif tipo == "PACK_DROP":
            return self.pack_drop()

        elif tipo == "IF":
            return self.if_comando()

        elif tipo == "WHILE":
            return self.while_comando()

        elif tipo == "REPEAT":
            return self.repeat_comando()

        else:
            token = self.atual()
            raise SyntaxError(
                f"Comando inesperado "
                f"'{token.valor}' "
                f"na linha {token.linha}, "
                f"coluna {token.coluna}"
            )

    # Movimento

    def movimento(self):
        token = self.avancar()
        return {
            "tipo": "MOVIMENTO",
            "direcao": token.tipo
        }
    
    # PackCat

    def pack_cat(self):
        token = self.esperar("PACK_CAT")
        return {
            "tipo": "PACK_CAT"
        }

    # PackDrop

    def pack_drop(self):
        token = self.esperar("PACK_DROP")
        return {
            "tipo": "PACK_DROP"
        }

    # IF

    def if_comando(self):
        self.esperar("IF")
        condicao = self.condicao()
        self.esperar("LBRACE")
        comandos_if = []

        while self.atual().tipo != "RBRACE":

            comandos_if.append(
                self.comando()
            )

        self.esperar("RBRACE")
        comandos_else = None

        if self.atual().tipo == "ELSE":
            self.esperar("ELSE")
            self.esperar("LBRACE")
            comandos_else = []
            while self.atual().tipo != "RBRACE":

                comandos_else.append(
                    self.comando()
                )
            self.esperar("RBRACE")

        return {
            "tipo": "IF",
            "condicao": condicao,
            "entao": comandos_if,
            "senao": comandos_else
        }
    
    # WHILE

    def while_comando(self):
        self.esperar("WHILE")
        condicao = self.condicao()
        self.esperar("LBRACE")
        comandos = []
        while self.atual().tipo != "RBRACE":

            comandos.append(
                self.comando()
            )
        self.esperar("RBRACE")
        return {
            "tipo": "WHILE",
            "condicao": condicao,
            "comandos": comandos
        }

    # REPEAT

    def repeat_comando(self):
        self.esperar("REPEAT")
        numero = self.esperar("NUMBER")
        self.esperar("LBRACE")
        comandos = []
        while self.atual().tipo != "RBRACE":
            comandos.append(
                self.comando()
            )
        self.esperar("RBRACE")
        return {
            "tipo": "REPEAT",
            "vezes": numero.valor,
            "comandos": comandos
        }

    # Condição

    def condicao(self):
        sensores = {
            "IF_WALL_UP",
            "IF_WALL_DOWN",
            "IF_WALL_LEFT",
            "IF_WALL_RIGHT",
            "PACK_SEE"
        }

        esquerda = self.atual()
        if esquerda.tipo not in sensores:
            raise SyntaxError(
                f"Esperada condição, "
                f"mas encontrado "
                f"'{esquerda.valor}' "
                f"na linha {esquerda.linha}, "
                f"coluna {esquerda.coluna}"
            )

        self.avancar()
        operador = self.atual()
        if operador.tipo not in {
            "EQUAL",
            "NOT_EQUAL"
        }:
            raise SyntaxError(
                f"Esperado '==' ou '!=' "
                f"na linha {operador.linha}, "
                f"coluna {operador.coluna}"
            )

        self.avancar()
        valor = self.atual()
        if valor.tipo not in {
            "TRUE",
            "FALSE"
        }:
            raise SyntaxError(
                f"Esperado 'true' ou 'false' "
                f"na linha {valor.linha}, "
                f"coluna {valor.coluna}"
            )
        
        self.avancar()
        return {
            "tipo": "CONDICAO",
            "esquerda": esquerda.tipo,
            "operador": operador.tipo,
            "direita": valor.tipo
        }