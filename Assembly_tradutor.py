
from AST_nodes import (
    Program,
    Movimento,
    PackCat,
    PackDrop,
    Condicao,
    If,
    While,
    Repeat
)


class Translator:

    def __init__(self):
        self.codigo = []
        self.contador_labels = 0

        # Posições de memória dos sensores
        self.sensores = {
            "IF_WALL_UP": (5, "$r5"),
            "IF_WALL_DOWN": (7, "$r5"),
            "IF_WALL_LEFT": (8, "$r5"),
            "IF_WALL_RIGHT": (6, "$r5"),
            "PACK_SEE": (4, "$r4")
        }

    # Adiciona uma instrução
    def emitir(self, instrucao):
        self.codigo.append(instrucao)

    # Cria identificadores internos para os desvios
    def nova_label(self, prefixo):
        label = f"{prefixo}_{self.contador_labels}"
        self.contador_labels += 1
        return label

    # Marca uma posição interna no código
    def marcar(self, label):
        self.codigo.append(("LABEL", label))

    # Emite um BEQ com destino interno
    def emitir_beq(self, rs, rt, destino):
        self.codigo.append(("BEQ", rs, rt, destino))

    # Emite um J com destino interno
    def emitir_j(self, destino):
        self.codigo.append(("J", destino))

    # Converte os desvios internos em endereços numéricos
    def resolver_desvios(self):

        enderecos = {}
        pc = 0

        # Primeira passagem: calcula os endereços
        for instrucao in self.codigo:

            if isinstance(instrucao, tuple):
                if instrucao[0] == "LABEL":
                    enderecos[instrucao[1]] = pc
                else:
                    pc += 1
            else:
                pc += 1

        # Segunda passagem: gera o Assembly final
        resultado = []
        pc = 0

        for instrucao in self.codigo:

            if isinstance(instrucao, tuple):

                tipo = instrucao[0]

                # BEQ utiliza deslocamento relativo
                if tipo == "BEQ":

                    rs = instrucao[1]
                    rt = instrucao[2]
                    destino = instrucao[3]

                    deslocamento = enderecos[destino] - pc - 1

                    if not -32 <= deslocamento <= 31:
                        raise ValueError(
                            "Deslocamento BEQ fora do limite de 6 bits."
                        )

                    resultado.append(
                        f"beq {rs}, {rt}, {deslocamento}"
                    )

                    pc += 1

                # J utiliza endereço absoluto
                elif tipo == "J":

                    destino = instrucao[1]
                    endereco = enderecos[destino]

                    resultado.append(
                        f"j {endereco}"
                    )

                    pc += 1

                # Labels internos não aparecem no Assembly
                elif tipo == "LABEL":
                    continue

            else:
                resultado.append(instrucao)
                pc += 1

        return "\n".join(resultado)

    # Traduz o programa inteiro
    def traduzir(self, programa):

        self.codigo = []
        self.contador_labels = 0

        # Carrega o estado inicial do robô
        self.emitir("lw $r1, 1($0)")
        self.emitir("lw $r2, 2($0)")
        self.emitir("lw $r3, 3($0)")

        # Traduz os comandos da AST
        self.visitar(programa.comandos)

        # Salva o estado final do robô
        self.emitir("sw $r1, 1($0)")
        self.emitir("sw $r2, 2($0)")
        self.emitir("sw $r3, 3($0)")

        return self.resolver_desvios()

    # Percorre os comandos da AST
    def visitar(self, comandos):

        for comando in comandos:

            if isinstance(comando, Movimento):
                self.traduzir_movimento(comando)

            elif isinstance(comando, PackCat):
                self.traduzir_pack_cat()

            elif isinstance(comando, PackDrop):
                self.traduzir_pack_drop()

            elif isinstance(comando, If):
                self.traduzir_if(comando)

            elif isinstance(comando, While):
                self.traduzir_while(comando)

            elif isinstance(comando, Repeat):
                self.traduzir_repeat(comando)

            else:
                raise TypeError(
                    f"Comando não reconhecido: {type(comando).__name__}"
                )

    # Traduz movimentos
    def traduzir_movimento(self, comando):

        direcao = comando.direcao

        movimentos = {
            "MV_UP": ("$r2", 1, 2),
            "MV_RIGHT": ("$r1", 1, 1),
            "MV_DOWN": ("$r2", -1, 2),
            "MV_LEFT": ("$r1", -1, 1)
        }

        if direcao not in movimentos:
            raise ValueError(
                f"Movimento desconhecido: {direcao}"
            )

        registrador, incremento, memoria = movimentos[direcao]

        self.emitir(
            f"addi {registrador}, {registrador}, {incremento}"
        )

        self.emitir(
            f"sw {registrador}, {memoria}($0)"
        )

    # Traduz coleta do pacote
    def traduzir_pack_cat(self):

        fim = self.nova_label("FIM_CAT")
        coletar = self.nova_label("COLETAR")

        self.emitir("lw $r3, 3($0)")

        self.emitir_beq("$r3", "$0", coletar)
        self.emitir_beq("$0", "$0", fim)

        self.marcar(coletar)

        self.emitir("addi $r3, $0, 1")
        self.emitir("sw $r3, 3($0)")

        self.marcar(fim)

    # Traduz entrega do pacote
    def traduzir_pack_drop(self):

        fim = self.nova_label("FIM_DROP")
        entregar = self.nova_label("ENTREGAR")

        self.emitir("lw $r3, 3($0)")
        self.emitir("addi $r6, $0, 1")

        self.emitir_beq("$r3", "$r6", entregar)
        self.emitir_beq("$0", "$0", fim)

        self.marcar(entregar)

        self.emitir("addi $r3, $0, 0")
        self.emitir("sw $r3, 3($0)")

        self.marcar(fim)

    # Traduz condições
    def traduzir_condicao(self, condicao, destino_falso):

        sensor = condicao.esquerda
        operador = condicao.operador
        valor = condicao.direita

        if sensor not in self.sensores:
            raise ValueError(
                f"Sensor desconhecido: {sensor}"
            )

        memoria, registrador = self.sensores[sensor]

        # Carrega o sensor da memória
        self.emitir(
            f"lw {registrador}, {memoria}($0)"
        )

        # Converte o valor booleano
        if valor is True or str(valor).upper() == "TRUE":
            esperado = 1

        elif valor is False or str(valor).upper() == "FALSE":
            esperado = 0

        else:
            raise ValueError(
                f"Valor booleano inválido: {valor}"
            )

        # Reconhece os operadores
        if operador in ("EQUAL", "=="):
            igualdade = True

        elif operador in ("NOT_EQUAL", "!="):
            igualdade = False

        else:
            raise ValueError(
                f"Operador inválido: {operador}"
            )

        # Verifica quando a condição é falsa
        if (igualdade and esperado == 1) or (
            not igualdade and esperado == 0
        ):

            # Condição falsa quando sensor = 0
            self.emitir_beq(
                registrador,
                "$0",
                destino_falso
            )

        else:

            # Condição falsa quando sensor = 1
            continuar = self.nova_label("CONTINUAR")

            self.emitir_beq(
                registrador,
                "$0",
                continuar
            )

            self.emitir_j(destino_falso)

            self.marcar(continuar)

    # Traduz IF e ELSE
    def traduzir_if(self, comando):

        label_else = self.nova_label("ELSE")
        label_fim = self.nova_label("ENDIF")

        destino_falso = (
            label_else
            if comando.senao is not None
            else label_fim
        )

        self.traduzir_condicao(
            comando.condicao,
            destino_falso
        )

        # Bloco IF
        self.visitar(comando.entao)

        if comando.senao is not None:

            self.emitir_j(label_fim)

            self.marcar(label_else)

            # Bloco ELSE
            self.visitar(comando.senao)

        self.marcar(label_fim)

    # Traduz WHILE
    def traduzir_while(self, comando):

        inicio = self.nova_label("WHILE")
        fim = self.nova_label("ENDWHILE")

        self.marcar(inicio)

        # Verifica a condição
        self.traduzir_condicao(
            comando.condicao,
            fim
        )

        # Executa o corpo
        self.visitar(comando.comandos)

        # Retorna ao início
        self.emitir_j(inicio)

        self.marcar(fim)

    # Verifica se o corpo utiliza o registrador r6
    def utiliza_r6(self, comandos):

        for comando in comandos:

            if isinstance(comando, PackDrop):
                return True

            elif isinstance(comando, Repeat):
                return True

            elif isinstance(comando, If):

                if self.utiliza_r6(comando.entao):
                    return True

                if comando.senao is not None:
                    if self.utiliza_r6(comando.senao):
                        return True

            elif isinstance(comando, While):

                if self.utiliza_r6(comando.comandos):
                    return True

        return False

    # Traduz REPEAT
    def traduzir_repeat(self, comando):

        numero = comando.vezes

        if numero <= 0:
            raise ValueError(
                "Repeat precisa ser maior que zero"
            )

        # O contador utiliza r6, conforme a tabela.
        # PackDrop também utiliza r6, portanto não
        # podem compartilhar o mesmo bloco Repeat.
        if self.utiliza_r6(comando.comandos):
            raise ValueError(
                "O bloco Repeat não pode conter PackDrop "
                "ou outro Repeat, pois utilizam o registrador r6."
            )

        inicio = self.nova_label("REPEAT")
        fim = self.nova_label("ENDREPEAT")

        # Inicializa o contador
        self.emitir(
            f"addi $r6, $0, {numero}"
        )

        self.marcar(inicio)

        # Verifica se o contador chegou a zero
        self.emitir_beq(
            "$r6",
            "$0",
            fim
        )

        # Executa os comandos do Repeat
        self.visitar(comando.comandos)

        # Decrementa o contador
        self.emitir(
            "addi $r6, $r6, -1"
        )

        # Retorna ao início
        self.emitir_j(inicio)

        self.marcar(fim)
        # Executa comandos do Repeat
        self.visitar(comando.comandos)

        # Decrementa contador
        self.emitir(f"LW $r6, {memoria}")
        self.emitir("ADDI $r6, $r6, -1")
        self.emitir(f"SW $r6, {memoria}")
        self.emitir(f"J {label_inicio}")
        self.emitir(f"{label_fim}:")