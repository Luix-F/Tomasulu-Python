# Simulador do Algoritmo de Tomasulo

Este projeto consiste em uma implementação do Algoritmo de Tomasulo, uma técnica de arquitetura de computadores que permite a execução fora de ordem de instruções. O simulador gerencia dependências de dados, realiza renomeação de registradores e especulação de desvios.

## Instruções Suportadas:

Aritméticas: ADD, SUB, MULT, DIV

Memória: LD (Load), SW (Store)

Controle (Branch): BEQ, BNE

Ciclo de Vida da Instrução: Issue (Despacho), Execução, Write Result (Escrita) e Commit.

Renomeação de Registradores: Implementada através da classe Rename para resolver dependências falsas (WAR e WAW).

Estações de Reserva: Filas dedicadas para ALU, Multiplicação, Memória e Branch.

Especulação de Desvio: Previsão de saltos para instruções BEQ e BNE.

## Métricas de Desempenho:

Cálculo de IPC (Instruções por Ciclo).

Contagem de Bolhas (Stalls) no pipeline.

Total de Ciclos de Clock executados.


## Como Usar

1. Pré-requisitos

Certifique-se de ter o Python 3 instalado em sua máquina.

2. Arquivo de Entrada

Altere o arquivo instruct.luix no mesmo diretório do script. O formato deve seguir o padrão:
OP, DESTINO, FONTE1, FONTE2

Exemplo de instruct.luix:

LD, $t1, 0, $t2
ADD, $t3, $t1, $t4
SUB, $t5, $t1, $t3
MULT, $t6, $t5, $t4
BEQ, $t1, $t2, 10
END


3. Executando

Execute o script principal via terminal:

python TomasuloSimulator.py


## Saída e Métricas

Ao final da execução, o simulador exibirá no console:

O estado final das instruções (tabela com tempos de Issue, Exec, Write e Commit).

Ciclos: Quantidade total de clocks gastos.

Bolhas: Quantidade de ciclos desperdiçados esperando dependências ou recursos.

IPC: Índice de Instruções por Ciclo (Eficiência do processador).

## Autores
- Ana Cristina Martins Silva
- Letícia Azevedo Cota Barbosa
- Lívia Alves Ferreira
- Lucas Gabriel Almeida Gomes
- Luiz Fernando Antunes da Silva Frassi


Desenvolvido como parte da disciplina de Arquitetura de Computadores III.

Este projeto é para fins educacionais, simulando o comportamento lógico do hardware.
