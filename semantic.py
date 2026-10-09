from AST_nodes import (If, While, Repeat,)

class SemanticAnalyzer:

    def analisar(self, programa):
        self.visitar(programa.comandos)

    def visitar(self, comandos):
        for comando in comandos:

            if isinstance(comando, Repeat):
                if comando.vezes <= 0: # detector de erro
                    raise ValueError("Repeat tem que ser maior que 0")
                self.visitar(comando.comandos)

            elif isinstance(comando, While):
                self.visitar(comando.comandos)

            elif isinstance(comando, If):
                self.visitar(comando.entao)

                if comando.senao is not None:
                    self.visitar(comando.senao)
