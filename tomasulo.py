class Instrucao:
    
    def __init__(self, nome, i, j, k, issue, exec_completa, write_result, tipo, posi, status):
        self.nome = nome
        self.i = i
        self.j = j
        self.k = k
        self.issue = issue
        self.exec_completa = exec_completa
        self.write_result = write_result
        self.tipo = tipo
        self.posi = posi
        self.status = status

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
        return regs1, self.Mem[posi]
        
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
                tipo= ty,
                posi= y,
                status= "none"
            )
            y = y + 1
            instrucoes_decodificadas.append(instrucao)
            
        return instrucoes_decodificadas
    
    def despacho(self, instrucoes, ufs, erALU, erMULT,erMEM, erBR):
        for u in ufs:  
            
            if u.Ocupado == False and u.nome == "ALU" and len(erALU) > 0 and self.sem_dependencias(instrucoes, erALU[0]):
                u.instrucao = erALU.pop(0)
                u.Ocupado = True
                u.vida = 0
                u.instrucao.status = "UF"

            if u.Ocupado == False and u.nome == "MULT" and len(erMULT) > 0 and self.sem_dependencias(instrucoes, erMULT[0]):
                u.instrucao = erMULT.pop(0)
                u.Ocupado = True
                u.vida = 0
                u.instrucao.status = "UF"

            if u.Ocupado == False and u.nome == "MEM" and len(erMEM) > 0 and self.sem_dependencias(instrucoes, erMEM[0]):
                u.instrucao = erMEM.pop(0)
                u.Ocupado = True
                u.vida = 0
                u.instrucao.status = "UF"

            if u.Ocupado == False and u.nome == "BR" and len(erBR) > 0 and self.sem_dependencias(instrucoes, erBR[0]):
                u.instrucao = erBR.pop(0)
                u.Ocupado = True
                u.vida = 0
                u.instrucao.status = "UF"
          
    def atualiza_clock(self, ufs, clock):
        tmpInst = Instrucao(0,0,0,0,0,0,0,0,0,0)
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
    
    def atualizar_inst(self, instrucoes, clock, m):
        for instr in instrucoes:
            if instr.exec_completa > -1 & instr.write_result == -1:
                instr.write_result = clock
                instr.status = "commit"
                if instr.tipo == "ADD":
                    m.setR(instr.i, (m.getR(instr.j) + m.getR(instr.k)))
                if instr.tipo == "SUB":
                    m.setR(instr.i, (m.getR(instr.j) - m.getR(instr.k)))
                if instr.tipo == "MULT":
                    m.setR(instr.i, (m.getR(instr.j) * m.getR(instr.k)))
                if instr.tipo == "DIV":
                    m.setR(instr.i, (m.getR(instr.j) / m.getR(instr.k)))

                if instr.tipo == "LD":
                    instr.i = m.getM(instr.i, instr.j, instr.k)
                    
                if instr.tipo == "SW":
                    m.setM(instr.i, instr.j, instr.k)
                    
                if instr.tipo == "BEQ":
                    if (m.getR(instr.j) == m.getR(instr.k)):
                        self # desvio
                if instr.tipo == "BNE":
                    if (m.getR(instr.j) != m.getR(instr.k)):
                        self # desvio
                
                


    def imprimir_tabela(self, instrucoes):
        print(f"{'Nome':<8} {'i':<3} {'j':<3} {'k':<3} {'Issue':<6} {'Exec':<6} {'Write':<6} {'Tipo':<6} {'Posi':<4} {'status':<6}")
        print("-" * 60)

        for inst in instrucoes:
            print(f"{inst.nome:<8} {inst.i:<3} {inst.j:<3} {inst.k:<3} "
                f"{inst.issue:<6} {inst.exec_completa:<6} {inst.write_result:<6} "
                f"{inst.tipo:<6} {inst.posi:<4} {inst.status:<6}")

    def sem_dependencias(self, instrucoes, instruc):#, i, j, k, posi):
        print("---------------------------------------")
        for i in range(instruc.posi):
            print(instrucoes[i].nome + instrucoes[i].i +" -- " + instruc.nome +" " + instruc.j + " " + instruc.k)
            if ((instruc.j == instrucoes[i].i or instruc.k == instrucoes[i].i )and instrucoes[i].exec_completa == -1):
                print("DEPENDECIA")
                return False
        print("sem dependencia")
        return True
        

    def simulador(self):
        
        #er = EstacaoDeReserva()
        clock = 0

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
        tmpInst = Instrucao(0,0,0,0,0,0,0,0,0,0) # TMP apenas para formato

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
        

        # ---- Tomasulu ---- # loop
        while instrucoes[-1].write_result < 0:
            for i in range(clock*2, 2 + clock*2):          # Instuçoes sao carregadas nas estacoes
                if i < len(instrucoes):
                    inst = instrucoes[i]
                    if inst.tipo == "ALU":
                        inst.issue = clock
                        inst.status = "ER"
                        erALU.append(inst)
                    elif inst.tipo == "MULT":
                        inst.issue = clock
                        inst.status = "ER"
                        erMULT.append(inst)
                    elif inst.tipo == "MEM":
                        inst.issue = clock
                        inst.status = "ER"
                        erMEM.append(inst)
                    elif inst.tipo == "BR":
                        inst.issue = clock
                        inst.status = "ER"
                        erBR.append(inst)
        
            # Despacho de instrucao
            self.atualizar_inst(instrucoes, clock, m)
            
            self.despacho(instrucoes, ufs, erALU, erMULT,erMEM, erBR)
            self.atualiza_clock(ufs, clock)
            

            print("---------------------------------------")
            print(clock)
            self.imprimir_tabela(instrucoes)
            clock = clock + 1
            #print(ufs[0].instrucao.exec_completa)
        #print(instrucoes[-1].write_result)



        # ---- Tomasulu ---- # loop

t = Tomasulo()
t.simulador()
