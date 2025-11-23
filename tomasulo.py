class Instrucao:
    
    def __init__(self, nome, i, j, k, issue, exec_completa, write_result, commit,tipo, posi, status, value, podeExecutar, previsao, rename):
        self.nome = nome
        self.i = i
        self.j = j
        self.k = k
        self.issue = issue
        self.exec_completa = exec_completa
        self.write_result = write_result
        self.commit = commit
        self.tipo = tipo
        self.posi = posi
        self.status = status
        self.value = value
        self.podeExecutar = podeExecutar
        self.previsao = previsao
        self.rename = rename

    def __str__(self):
        return (f"Instrução: {self.nome}, i: {self.i}, j: {self.j}, k: {self.k}, "
            f"Issue: {self.issue if self.issue is not None else 'N/A'}, "
            f"Exec. Completa: {self.exec_completa if self.exec_completa is not None else 'N/A'}, "
            f"Write Result: {self.write_result if self.write_result is not None else 'N/A'}")
    
    def to_dict(self):
        """
        Retorna a instrução como um dicionário.
        """
        return {
            "Instrução": self.nome,
            "i": self.i,
            "j": self.j,
            "k": self.k,
            "Issue": self.issue,
            "Exec. Completa": self.exec_completa,
            "Write Result": self.write_result
        }

class Unidades_Funcionais:
    def __init__(self, nome, tempo, instrucao, Ocupado, vida):
        self.nome = nome
        self.tempo = tempo
        self.instrucao = instrucao
        self.Ocupado = Ocupado
        #self.id = id
        self.vida = vida
        #self.qtd = qtd
    def _start_(self, nome, tempo, Ocupado):
        self.nome = nome
        self.tempo = tempo
        self.Ocupado = Ocupado

class Memory:
    Reg = []
    Mem = []
    def __init__(self):
        for i in range(20):
            self.Reg.append(i)
        for i in range(200):
            self.Mem.append(i)

    def getM(self, regs1, regs2, regs3):
        posi = self.getR(regs3) + int(regs2)
        self.setR(regs1, self.Mem[posi])
        return self.Mem[posi]
        
    def setM(self, regs1, regs2, regs3):
        posi = self.getR(regs3) + int(regs2)
        self.Mem[posi] = self.getR(regs1)

    def getR(self, regs):
        if "$t" in regs:
            #regs = ""
            regs = regs.replace("$", "").replace("t", "")
            p = int(regs)
            return self.Reg[p]
        
    def setR(self, regs, value):
        if "$t" in regs:
            #regs = ""
            regs = regs.replace("$", "").replace("t", "")
            p = int(regs)
            self.Reg[p] = value

class Rename:
    Renome = []
    def __init__(self):

        # rename - Rgs - Value
        self.Renome = [
        ["Ra", -1, -1],
        ["Rb", -1, -1],
        ["Rc", -1, -1],
        ["Rd", -1, -1],
        ["Re", -1, -1],
        ["Rf", -1, -1]
        ]
    def set(self, r1):
        for r in self.Renome:
            if r[1] == -1:
                r[1] = r1
                #r[2] = r1.getR(r1)
                return r[0]
            
    def setValue(self, re, value):
        for r in self.Renome:
            if r[0] == re:
                r[2] = value
            
    def clear(self, re):
        for r in self.Renome:
            if r[0] == re:
                r[1] = -1
                r[2] = -1
    def value(self, re):
        for r in self.Renome:
            if r[0] == re:
                return r[2]


class Tomasulo:

    def ler_arquivo(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
            return conteudo
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
            return None
        except Exception as e:
            print(f"Ocorreu um erro ao ler o arquivo: {e}")
            return None
        
    def decodificar_instrucoes(self, conteudo_instrucoes):

        instrucoes_decodificadas = []
        
        if not conteudo_instrucoes:
            print("Conteúdo das instruções está vazio.")
            return instrucoes_decodificadas

        # Divide o conteúdo em linhas
        linhas = conteudo_instrucoes.strip().split('\n')

        y = 0
        
        for linha in linhas:
            # Remove espaços em branco e verifica se a linha não está vazia
            linha_limpa = linha.strip()
            if not linha_limpa or linha_limpa.lower() == 'end':
                # Ignora linhas vazias e a instrução 'end'
                continue

            # Divide a linha pelos delimitadores (vírgula e espaço)
            partes = [p.strip() for p in linha_limpa.split(',')]
            
            # Garante que temos pelo menos 4 partes (NOME, i, j, k)
            if len(partes) < 4:
                print(f"Aviso: Linha de instrução ignorada por formato inválido: {linha_limpa}")
                continue

            nome = partes[0]
            i = partes[1]
            j = partes[2]
            k = partes[3]

            ty = ""
            if nome == "ADD" or nome == "SUB":
                ty = "ALU"
            elif nome == "MULT" or nome == "DIV":
                ty = "MULT"
            elif nome == "BEQ" or nome == "BNE":
                ty = "BR"
            elif nome == "LD" or nome == "SW":
                ty = "MEM"

            # Cria a instância da Instrucao. Os campos de ciclo (para a simulação de Tomasulo)
            # são inicializados como None, pois serão preenchidos durante a execução.
            instrucao = Instrucao(
                nome=nome,
                i=i,
                j=j,
                k=k,
                issue= -1,          # Será definido quando a instrução for emitida
                exec_completa= -1,  # Será definido quando a execução terminar
                write_result= -1,   # Será definido quando o resultado for escrito
                commit = -1,
                tipo= ty,
                posi= y,
                status= "none",
                value= "null",
                podeExecutar = True,
                previsao = -1,
                rename = nome
            )
            y = y + 1
            instrucoes_decodificadas.append(instrucao)
            
        return instrucoes_decodificadas
    
    def despacho(self, instrucoes, ufs, erALU, erMULT,erMEM, erBR, renomeado):
        for u in ufs:  
            
            if u.Ocupado == False and u.nome == "ALU" and len(erALU) > 0:
                saida = False
                
                for y in range(len(erALU)):
                    if not saida:
                        if erALU[y].podeExecutar and u.Ocupado == False and self.sem_dependencias(instrucoes, erALU[y]):
                            if not self.sem_falsa_dependencia(instrucoes, erALU[y]) and erALU[y].exec_completa == -1:
                                erALU[y].rename = renomeado.set(erALU[y])
                            u.instrucao = erALU.pop(y)
                            u.Ocupado = True
                            u.vida = 0
                            u.instrucao.status = "UF"
                            saida = True

            if u.Ocupado == False and u.nome == "MULT" and len(erMULT) > 0:
                saida = False
                
                for y in range(len(erMULT)):
                    if not saida:
                        if erMULT[y].podeExecutar and u.Ocupado == False and self.sem_dependencias(instrucoes, erMULT[0]):
                            if not self.sem_falsa_dependencia(instrucoes, erMULT[y]) and erMULT[y].exec_completa == -1:
                                erMULT[y].rename = renomeado.set(erMULT[y])
                            u.instrucao = erMULT.pop(y)
                            u.Ocupado = True
                            u.vida = 0
                            u.instrucao.status = "UF"
                            saida = True

            if u.Ocupado == False and u.nome == "MEM" and len(erMEM) > 0:
                saida = False
                
                for y in range(len(erMEM)):
                    if not saida:
                        if erMEM[y].podeExecutar and u.Ocupado == False and self.sem_dependencias(instrucoes, erMEM[0]):
                            if not self.sem_falsa_dependencia(instrucoes, erMEM[y]) and erMEM[y].exec_completa == -1:
                                erMEM[y].rename = renomeado.set(erMEM[y])
                            u.instrucao = erMEM.pop(y)
                            u.Ocupado = True
                            u.vida = 0
                            u.instrucao.status = "UF"
                            saida = True

            if u.Ocupado == False and u.nome == "BR" and len(erBR) > 0:
                saida = False
                
                for y in range(len(erBR)):
                    if not saida:
                        if erBR[y].podeExecutar and u.Ocupado == False and self.sem_dependencias(instrucoes, erBR[0]):
                            if not self.sem_falsa_dependencia(instrucoes, erBR[y]) and erBR[y].exec_completa == -1:
                                erBR[y].rename = renomeado.set(erBR[y])
                            u.instrucao = erBR.pop(y)
                            u.Ocupado = True
                            u.vida = 0
                            u.instrucao.status = "UF"
                            saida = True
          
    def atualiza_clock(self, ufs, clock):
        tmpInst = Instrucao(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        for u in ufs:
            if u.Ocupado == True and u.instrucao.exec_completa == -1:
                if u.tempo == u.vida:
                    u.Ocupado = False
                    u.vida = 0
                    u.instrucao.exec_completa = clock
                    u.instrucao = tmpInst
                else:
                    u.vida = u.vida + 1
                    #u.instrucao.exec_completa = 10

    def verifica_desvio(self, posi, instrucoes):
        #print(posi)
        for i in range(posi):
            #print("\n\n")
            #print(instrucoes[i].tipo)
            if instrucoes[i].tipo == "BR" and instrucoes[i].exec_completa == -1:
                return False
        return True
        
    def WR(self, instrucoes, clock, previsao, m, pc):
        for instr in instrucoes:
            if instr.exec_completa > -1 and instr.write_result == -1 and instr.podeExecutar:
                instr.write_result = clock
                instr.status = "Write Result"
                print(instr.nome)
                print("Write Result")
                
    def atualizar_inst(self, instrucoes, clock, m, renomeado, previsao):
        for instr in instrucoes:
            if instr.write_result > -1 and instr.commit == -1 and self.verifica_desvio(instr.posi, instrucoes) and instr.podeExecutar == True:
                instr.commit = clock
                instr.status = "commit"
                if instr.rename != instr.nome:
                    renomeado.clear(instr.rename)
                    instr.rename = instr.nome

                if instr.nome == "ADD":
                    m.setR(instr.i, (m.getR(instr.j) + m.getR(instr.k)))
                if instr.nome == "SUB":
                    m.setR(instr.i, (m.getR(instr.j) - m.getR(instr.k)))
                if instr.nome == "MULT":
                    m.setR(instr.i, (m.getR(instr.j) * m.getR(instr.k)))
                if instr.nome == "DIV":
                    m.setR(instr.i, (m.getR(instr.j) / m.getR(instr.k)))

                if instr.nome == "LD":
                    instr.i = m.getM(instr.i, instr.j, instr.k)
                    
                if instr.nome == "SW":
                    m.setM(instr.i, instr.j, instr.k)
                    
                if instr.nome == "BEQ":
                    
                    if (m.getR(instr.j) == m.getR(instr.k) and instr.previsao == 0):
                        #pc[0] = instr.posi
                        previsao[0] = 1
                        for y in range(instr.posi+1, instr.posi+int(instr.i)):
                            instrucoes[y].podeExecutar = False
                            instrucoes[y].status = "nop"
                        for y in range(instr.posi+1, len(instrucoes)):
                            instrucoes[y].issue = -1 
                            instrucoes[y].exec_completa = -1 
                            instrucoes[y].write_result = -1 
                            instrucoes[y].commit = -1
                    elif (m.getR(instr.j) != m.getR(instr.k) and instr.previsao == 1):
                        #pc[0] = instr.posi
                        previsao[0] = 0
                        for y in range(instr.posi+1, len(instrucoes)):
                            instrucoes[y].issue = -1 
                            instrucoes[y].exec_completa = -1 
                            instrucoes[y].write_result = -1 
                            instrucoes[y].commit = -1
                        '''
                        print("\n\n\n\n")
                        for y in range(instr.posi+1, instr.posi+int(instr.i)):
                            instrucoes[y].podeExecutar = False
                            instrucoes[y].status = "nop"
                        #pc[0] + int(instr.i)'''
                if instr.nome == "BNE":
                    if (m.getR(instr.j) != m.getR(instr.k) and instr.previsao == 0):
                        #pc[0] = instr.posi
                        previsao[0] = 1
                        for y in range(instr.posi+1, instr.posi+int(instr.i)):
                            instrucoes[y].podeExecutar = False
                            instrucoes[y].status = "nop"
                        for y in range(instr.posi+1, len(instrucoes)):
                            instrucoes[y].issue = -1 
                            instrucoes[y].exec_completa = -1 
                            instrucoes[y].write_result = -1 
                            instrucoes[y].commit = -1
                    elif (m.getR(instr.j) != m.getR(instr.k) and instr.previsao == 1):
                        #pc[0] = instr.posi
                        previsao[0] = 0
                        for y in range(instr.posi+1, len(instrucoes)):
                            instrucoes[y].issue = -1 
                            instrucoes[y].exec_completa = -1 
                            instrucoes[y].write_result = -1 
                            instrucoes[y].commit = -1

    def imprimir_tabela(self, instrucoes):
        print(f"{'Nome':<12} {'i':<3} {'j':<3} {'k':<3} "
            f"{'Issue':<10} {'Exec':<6} {'Write':<7} {'Commit':<10} "
            f"{'Tipo':<8} {'Posi':<5} {'Status':<12} {'Value':<8} "
            f"{'PodeExec':<10} {'Previsao':<12} {'Rename':<10}")

        print("-" * 135)

        for inst in instrucoes:
            print(f"{inst.nome:<12} {inst.i:<3} {inst.j:<3} {inst.k:<3} "
                f"{inst.issue:<10} {str(inst.exec_completa):<6} {str(inst.write_result):<7} {str(inst.commit):<10} "
                f"{inst.tipo:<8} {inst.posi:<5} {inst.status:<12} {str(inst.value):<8} "
                f"{str(inst.podeExecutar):<10} {str(inst.previsao):<12} {str(inst.rename):<10}")


    def sem_dependencias(self, instrucoes, instruc):#, i, j, k, posi):
        print("---------------------------------------")
        for i in range(instruc.posi):
            #print(instrucoes[i].nome + instrucoes[i].i +" -- " + instruc.nome +" " + instruc.j + " " + instruc.k)
            if ((instruc.j == instrucoes[i].i or instruc.k == instrucoes[i].i )and instrucoes[i].exec_completa == -1): # verifica dependencia verdadeira
                print("DEPENDECIA")
                return False
        print("sem dependencia")
        return True
        
    def sem_falsa_dependencia(self, instrucoes, instruc):
        print("---------------------------------------")
        for i in range(instruc.posi):
            #print(instrucoes[i].nome + instrucoes[i].i +" -- " + instruc.nome +" " + instruc.j + " " + instruc.k)
            if ((instruc.i == instrucoes[i].j or instruc.i == instrucoes[i].k) and instrucoes[i].exec_completa == -1):
            #if ((instruc.j == instrucoes[i].i or instruc.k == instrucoes[i].i )and instrucoes[i].exec_completa == -1): # verifica dependencia verdadeira
                print("FALSE _ DEPENDECIA")
                return False
        print("sem falsa dependencia")
        return True

    def especulacao(self, posi, instrucoes, previsao, pc):
        if instrucoes[posi].tipo == "BR":
            
            if previsao[0] == 1:
                instrucoes[posi].previsao = 1
                print("\n\nC#########################################################$\n\n")
                print(instrucoes[posi].nome)
                print(previsao[0])
                if instrucoes[posi].nome == "BEQ":
                    #if (m.getR(instr.j) == m.getR(instr.k)):
                    
                    for y in range(posi+1, posi+int(instrucoes[posi].i)):
                        instrucoes[y].podeExecutar = False
                        instrucoes[y].status = "nop"
                        #pc[0] + int(instr.i)
                if instrucoes[posi].nome == "BNE":
                    #if (m.getR(instr.j) != m.getR(instr.k)):
                    #for y in range(pc[0]+1, pc[0]+int(instrucoes[posi].i)):
                    for y in range(posi+1, posi+int(instrucoes[posi].i)):
                        instrucoes[y].podeExecutar = False
                        instrucoes[y].status = "nop"
                        #pc[0] + int(instr.i) 
            else:
                instrucoes[posi].previsao = 0
                print("\n\nC************************************************************n\n")

    def verifica_parada(self, instrucoes, pc):
    
        # Retorna True se a simulação deve parar, False caso contrário.
        
        # Verifica se ainda há instruções para buscar
        # Se o PC for menor que o total de instruções, ainda tem o que fazer.
        if pc[0] < len(instrucoes):
            return False
        #return instrucoes[-1].status == "commit"
        return not any(obj.status not in ("commit", "nop") for obj in instrucoes)
     
    def simulador(self):
        
        #er = EstacaoDeReserva()
        clock = 0
        pc = []
        pc.append(0)

        previsao = []
        previsao.append(0)

        # Registrador de renomeacao
        renomeado = Rename()
        renomeado.__init__()

        caminho = './instruct.luix'
        conteudo = self.ler_arquivo(caminho)
        instrucoes = self.decodificar_instrucoes(conteudo)

        # Estacoes de reserva
        erALU = []
        erMULT = []
        erMEM = []
        erBR = []

        # Registradores e memoria
        m = Memory()
        m.__init__()

        # unidades funcionais
        ufs = [] 
        tmpInst = Instrucao(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0) # TMP apenas para formato

        ufALU_1 = Unidades_Funcionais('ALU', 2 -1, tmpInst, False, 0)
        #ufALU_1._start_("ALU", 2, False)
        ufALU_2 = Unidades_Funcionais('ALU', 2 -1, tmpInst, False, 0)
        #ufALU_2._start_("ALU", 2, False)

        ufMULT = Unidades_Funcionais('MULT', 6 -1, tmpInst, False, 0)
        #ufMULT._start_("MULT", 6, False)

        ufMEM = Unidades_Funcionais('MEM', 4 -1, tmpInst, False, 0)
        #ufMEM._start_("MEM", 4, False)

        ufBR = Unidades_Funcionais('BR', 1 -1, tmpInst, False, 0)
        #ufBR._start_("BR", 1, False)

        ufs = [ufALU_1, ufALU_2, ufMULT, ufMEM, ufBR]
        

        # ---- Tomasulo ---- # loop
        while not self.verifica_parada(instrucoes,pc): # condicao de parada
            for i in range(pc[0], pc[0]+2):             # Instuçoes sao carregadas nas estacoes
                if i < len(instrucoes):
                    inst = instrucoes[i]
                    if inst.tipo == "ALU" and inst.podeExecutar:
                        inst.issue = clock
                        inst.status = "ER"
                        erALU.append(inst)
                    elif inst.tipo == "MULT" and inst.podeExecutar:
                        inst.issue = clock
                        inst.status = "ER"
                        erMULT.append(inst)
                    elif inst.tipo == "MEM" and inst.podeExecutar:
                        inst.issue = clock
                        inst.status = "ER"
                        erMEM.append(inst)
                    elif inst.tipo == "BR" and inst.podeExecutar:
                        inst.issue = clock
                        inst.status = "ER"
                        erBR.append(inst)
                        self.especulacao(inst.posi, instrucoes, previsao, pc)
            if pc[0] < len(instrucoes):
                pc[0] = pc[0] +2
        
            
            self.WR(instrucoes, clock, previsao, m, pc)
            self.atualizar_inst(instrucoes, clock, m, renomeado, previsao)
            
            self.despacho(instrucoes, ufs, erALU, erMULT,erMEM, erBR, renomeado)
            self.atualiza_clock(ufs, clock)
            

            print("---------------------------------------")
            print(f"{clock} __ {pc[0]}" )
            self.imprimir_tabela(instrucoes)
            clock = clock + 1
            #print(ufs[0].instrucao.exec_completa)
        #print(instrucoes[-1].write_result)



        # ---- Tomasulu ---- # loop

t = Tomasulo()
t.simulador()

'''

Renomeacao ---
ajuste de interface
etc...
'''