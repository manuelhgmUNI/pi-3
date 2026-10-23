identificadores = {"add","sub","and","or","addi","lw","sw","beq","j"}

def asm_bin(codigo):
    linha = codigo.splitlines()
    bin [linha.len] = {}
    for i in range (linha.len):
        palavras = linha[i].split(" ")
        ID = palavras[0]
        match ID:
            # R - tipo | rs | rt | rd | funct
            case "add": #0000/000 (add $rd, $rs, $rt)
                bin += "0000"+palavras[2]+palavras[3]+palavras[1]+"000"
            case "sub": #0000/010 (sub $rd, $rs, $rt)
                bin += "0000"+palavras[2]+palavras[3]+palavras[1]+"010"
            case "and": #0000/100 (add $rd, $rs, $rt)
                bin += "0000"+palavras[2]+palavras[3]+palavras[1]+"100"
            case "or":  #0000/101 (or $rd, $rs, $rt)
                bin += "0000"+palavras[2]+palavras[3]+palavras[1]+"101"
            
            # I
            case "addi":

            case "lw":

            case "sw":

            case "beq":

            # J
            case "j":


        