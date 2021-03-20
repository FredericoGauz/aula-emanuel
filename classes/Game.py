from classes.ObjetoDoMundo import ObjetoDoMundo
from classes.atores.atores import Bandido
from classes.Mundo import Mundo
import utilidades
import sys
import random
import msvcrt

import graficos


class Game:
    mundo: Mundo

    def __init__(self, mundo):
        self.mundo = mundo

    def getBandidos(self):
        return self.mundo.getItemPorSimbolo(graficos.graficos['simbolos']['bandido'])

    def moveObjeto(self, objeto: ObjetoDoMundo, x:int, y:int):

        # checa se está querendo continuar parado
        if x == 0 and y == 0:
            return

        # soma a posição anterior mais o vetor de movimento 'x' e 'y'
        paraX = objeto.x + x
        paraY = objeto.y + y

        # checa se movimento já está impedido
        if paraX == self.mundo.comprimento() - 1 and paraY == self.mundo.profundidade() - 1:
            return

        # checa se o para{x ou y} é maior que o comprimento e profundidade do mundo

        paraX = utilidades.clamp(paraX, 0, self.mundo.comprimento() - 1)
        paraY = utilidades.clamp(paraY, 0, self.mundo.profundidade() - 1)

        self.mundo.moveObjeto(
            objeto, paraX, paraY)

    def pegaOInputDoTurno(self):
        # recebe o input
        # recebe uma caracter (ex. a, s, k, 1, v) sem o usuário precisar dar 'Enter'
        char = msvcrt.getwch()

        # se for '0' sai do jogo
        if char == '0':
            print('Adios!!!')
            sys.exit()
        return char
    
    # No turno do bandido (AI)
    # Procurar o Heroi
    # Calcular a menor distancia para chegar ao Heroi
    # Se mover em direção a ele
    # Mais tarde, ele pode também levar em consideração a posição atual do segundo bandido
    def turnoBandido(self, bandido:ObjetoDoMundo):
        # posição do herói após a jogada dele
        heroi = self.mundo.getItemPorSimbolo('@')[0]
        
        # diferença entre a sua posição e a do herói
        deltaX = (heroi.x or 0)  - (bandido.x or 0)
        deltaY = (heroi.y or 0) - (bandido.y or 0)

        #sua velocidade
        velocidade = 1

        # suas jogadas
        self.moveObjeto(
            bandido, 
            
            # PARA FAZER: limita a movimentação baseado na posição do herói. Ex. mesmo que você possa andar mais que a distancia entre você e o herói, você não ultrapassa ele
            velocidade if deltaX > 0 else -velocidade ,
            velocidade if deltaY > 0 else -velocidade ,
            )

    def turnoLogico(self):
        char = self.pegaOInputDoTurno()

        # procura vetor de movimento
        direction = utilidades.getDirection(char)

        # se não tiver vetor de movimento (direção) retorna
        if direction == None:
            print('Esse caminho não vai para lugar nenhum.')
            return

        # roda os turnos dos personagens

        # pega o herois (no caso só tem um)
        lista = self.mundo.getItemPorSimbolo(
            graficos.graficos['simbolos']['heroi'])
        heroi = lista[0]

        # move o herói baseado no movimento escolhido
        self.moveObjeto(heroi, direction[0], direction[1])

        # pega os outros personagens
        for bandido in self.getBandidos():
            self.turnoBandido(bandido)
            
    def turnoTotal(self, turno: int):
        # se for o turno inicial gera o mapa antes do primeiro movimento
        if turno != 0:
            # turno lógico
            self.turnoLogico()

        # aumenta o número do turno
        turno += 1

        # gera as primeiras instruções
        instrucoes = self.mundo.geraInstrucoes()

        # gera as dimensões do jogo
        dimensoes = utilidades.geraDimensoes(
            self.mundo.comprimento(), self.mundo.profundidade())
        self.turnoGrafico(dimensoes, instrucoes, self.mundo)

        # ver se o player venceu
        if len(self.mundo.items) == 1:
            print("Parabéns, o %s venceu!" % self.mundo.items[0].objeto.nome)
            return turno, True
        return turno, False

    def turnoGrafico(self, dimensoes, instrucoes, mundo: Mundo):
        # limpa a tela
        utilidades.clear()

        # cria a legenda
        for item in mundo.getItens():
            print(item.objeto.simbolo, ' => ', item.objeto.nome)

        print('\n')

        graficos.mostraTabuleiro(dimensoes, instrucoes)
