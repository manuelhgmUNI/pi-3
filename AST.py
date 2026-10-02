class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, nome, comandos):
        self.nome = nome
        self.comandos = comandos

class Movimento(ASTNode):
    def __init__(self, direcao):
        self.direcao = direcao

class PackCat(ASTNode):
    pass

class PackDrop(ASTNode):
    pass

class Condicao(ASTNode):
    def __init__(self, esquerda, operador, direita):
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita

class If(ASTNode):

    def __init__(self, condicao, entao, senao=None):
        self.condicao = condicao
        self.entao = entao
        self.senao = senao

class While(ASTNode):
    def __init__(self, condicao, comandos):
        self.condicao = condicao
        self.comandos = comandos

class Repeat(ASTNode):
    def __init__(self, vezes, comandos):
        self.vezes = vezes
        self.comandos = comandos