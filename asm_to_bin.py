tipo_R = {"add","sub","and","or"}
tipo_I = {"addi","lw","sw","beq"}
tipo_J = ["j"]

def asm_bin(codigo):
    codigo = codigo.replace(",", "")
    linha = codigo.splitlines()
    cbin = []
    for i in range (len(linha)):
        palavras = linha[i].split(" ")
        #print(palavras)
        ID = palavras[0]

        if ID in tipo_R:
            rd = format(int(reg_to_num(palavras[1])), "03b")
            rs = format(int(reg_to_num(palavras[2])), "03b")
            rt = format(int(reg_to_num(palavras[3])), "03b")

        if ID in tipo_I:
            rt = format(int(reg_to_num(palavras[1])), "03b")

        match ID:
            # R - tipo 4 | rs 3 | rt 3 | rd 3 | funct 3

            case "add": #0000/000 (add $rd, $rs, $rt)
                cbin.append("0000"+rs+rt+rd+"000")
            case "sub": #0000/010 (sub $rd, $rs, $rt)
                cbin.append("0000"+rs+rt+rd+"010")
            case "and": #0000/100 (add $rd, $rs, $rt)
                cbin.append("0000"+rs+rt+rd+"100")
            case "or":  #0000/101 (or $rd, $rs, $rt)
                cbin.append("0000"+rs+rt+rd+"101")
            
            # I tipo 4 | rt 3 | rs 3 | imm 6

            case "addi": #addi $rt, $rs, imm
                rs =  format(int((reg_to_num(palavras[2]))), "03b")
                imm = format(int(palavras[3]), "06b")

                cbin.append("0100"+rt+rs+imm)

            case "lw":   #lw $rt, imm($rs) 
                x =   palavras[2].split("(")
                rs =  format(int(reg_to_num(x[1].replace(")", ""))), "03b")
                imm = format(int(x[0]), "06b")

                cbin.append("1011"+rt+rs+imm)

            case "sw":   #sw $rt, imm($rs) 
                x =   palavras[2].split("(")
                rs =  format(int(reg_to_num(x[1].replace(")", ""))), "03b")
                imm = format(int(x[0]), "06b")

                cbin.append("1111"+rt+rs+imm)

            case "beq":  #beq $rt, $rs, imm
                rs =  format(int(reg_to_num(palavras[2])), "03b")
                imm = format(int(palavras[3]), "06b")

                cbin.append("1000"+rt+rs+imm)
            # J
            case "j":
                cbin.append("0010"+format(palavras[1], "07b"))

    return cbin


def reg_to_num(reg):
    if reg in {"SWs", "LEDs"}:
        return "7"

    return reg.replace("$", "").replace("r", "")