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
        self.contador_repeat = 0

        # Comandos enviados ao robô
        self.movimentos = {
            "MV_UP": 1,
            "MV_DOWN": 2,
            "MV_LEFT": 3,
            "MV_RIGHT": 4
        }

        # Sensores do robô
        self.sensores = {
            "IF_WALL_UP": 1,
            "IF_WALL_DOWN": 2,
            "IF_WALL_LEFT": 3,
            "IF_WALL_RIGHT": 4,
            "PACK_SEE": 5
        }

    # Adiciona uma instrução ao Assembly
    def emitir(self, instrucao):
        self.codigo.append(instrucao)

    # Cria labels automaticamente
    def nova_label(self, prefixo):
        label = f"{prefixo}_{self.contador_labels}"
        self.contador_labels += 1
        return label

    # Traduz o programa inteiro
    def traduzir(self, programa):
        self.codigo = []
        self.contador_labels = 0
        self.contador_repeat = 0
        self.emitir(".text")
        self.emitir("main:")

        # Carrega o estado inicial do robô
        self.emitir("LW $r1, POS_X")
        self.emitir("LW $r2, POS_Y")
        self.emitir("LW $r3, ESTADO_PACOTE")
        self.emitir("LW $r4, DESTINO_X")
        self.emitir("LW $r5, DESTINO_Y")

        # Traduz os comandos da AST
        self.visitar(programa.comandos)

        # Salva o estado final
        self.emitir("SW $r1, POS_X")
        self.emitir("SW $r2, POS_Y")
        self.emitir("SW $r3, ESTADO_PACOTE")
        self.emitir("FIM:")
        self.emitir("J FIM")
        return "\n".join(self.codigo)

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
        if direcao not in self.movimentos:
            raise ValueError(f"Movimento desconhecido: {direcao}")
        valor = self.movimentos[direcao]

        # Envia comando para o robô
        self.emitir(f"ADDI $r6, $r0, {valor}")
        self.emitir("SW $r6, IO_CMD")

        # Atualiza posição
        if direcao == "MV_UP":
            self.emitir("ADDI $r2, $r2, -1")
        elif direcao == "MV_DOWN":
            self.emitir("ADDI $r2, $r2, 1")
        elif direcao == "MV_LEFT":
            self.emitir("ADDI $r1, $r1, -1")
        elif direcao == "MV_RIGHT":
            self.emitir("ADDI $r1, $r1, 1")

    # Traduz coleta do pacote
    def traduzir_pack_cat(self):
        self.emitir("ADDI $r6, $r0, 5")
        self.emitir("SW $r6, IO_CMD")

        # Estado do pacote = 1
        self.emitir("ADDI $r3, $r0, 1")

    # Traduz entrega do pacote
    def traduzir_pack_drop(self):
        self.emitir("ADDI $r6, $r0, 6")
        self.emitir("SW $r6, IO_CMD")

        # Estado do pacote = 0
        self.emitir("ADDI $r3, $r0, 0")

    # Consulta sensor e desvia quando a condição for falsa
    def traduzir_condicao(self, condicao, label_falso):
        sensor = condicao.esquerda
        operador = condicao.operador
        valor = condicao.direita
        if sensor not in self.sensores:
            raise ValueError(f"Sensor desconhecido: {sensor}")
        codigo_sensor = self.sensores[sensor]

        # Seleciona o sensor
        self.emitir(f"ADDI $r6, $r0, {codigo_sensor}")
        self.emitir("SW $r6, IO_SELECT")

        # Lê o resultado do sensor
        self.emitir("LW $r7, IO_SENSOR")

        # Traduz true e false
        if valor == "TRUE":
            esperado = 1
        elif valor == "FALSE":
            esperado = 0
        else:
            raise ValueError(f"Valor booleano inválido: {valor}")

        # == e !=
        if operador == "EQUAL":
            if esperado == 1:
                self.emitir(f"BEQ $r7, $r0, {label_falso}")
            else:
                self.emitir(f"BNE $r7, $r0, {label_falso}")
        elif operador == "NOT_EQUAL":
            if esperado == 1:
                self.emitir(f"BNE $r7, $r0, {label_falso}")
            else:
                self.emitir(f"BEQ $r7, $r0, {label_falso}")
        else:
            raise ValueError(f"Operador inválido: {operador}")

    # Traduz IF e ELSE
    def traduzir_if(self, comando):
        label_else = self.nova_label("ELSE")
        label_fim = self.nova_label("ENDIF")
        self.traduzir_condicao(
            comando.condicao,
            label_else
        )

        # Bloco IF
        self.visitar(comando.entao)
        if comando.senao is not None:
            self.emitir(f"J {label_fim}")
            self.emitir(f"{label_else}:")

            # Bloco ELSE
            self.visitar(comando.senao)
        self.emitir(f"{label_else}:" if comando.senao is None else f"{label_fim}:")

    # Traduz WHILE
    def traduzir_while(self, comando):
        label_inicio = self.nova_label("WHILE")
        label_fim = self.nova_label("ENDWHILE")
        self.emitir(f"{label_inicio}:")

        # Verifica condição a cada repetição
        self.traduzir_condicao(
            comando.condicao,
            label_fim
        )
        self.visitar(comando.comandos)
        self.emitir(f"J {label_inicio}")
        self.emitir(f"{label_fim}:")

    # Traduz REPEAT
    def traduzir_repeat(self, comando):
        numero = comando.vezes
        if numero <= 0:
            raise ValueError(
                "Repeat precisa ser maior que zero"
            )
        identificador = self.contador_repeat
        self.contador_repeat += 1
        memoria = f"CONTADOR_{identificador}"
        label_inicio = self.nova_label("REPEAT")
        label_fim = self.nova_label("ENDREPEAT")

        # Inicializa contador
        self.emitir(f"ADDI $r6, $r0, {numero}")
        self.emitir(f"SW $r6, {memoria}")
        self.emitir(f"{label_inicio}:")
        self.emitir(f"LW $r6, {memoria}")
        self.emitir(f"BEQ $r6, $r0, {label_fim}")

        # Executa comandos do Repeat
        self.visitar(comando.comandos)

        # Decrementa contador
        self.emitir(f"LW $r6, {memoria}")
        self.emitir("ADDI $r6, $r6, -1")
        self.emitir(f"SW $r6, {memoria}")
        self.emitir(f"J {label_inicio}")
        self.emitir(f"{label_fim}:")