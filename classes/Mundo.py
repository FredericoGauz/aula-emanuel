"""
O Mundo é equivalente as instruções.

Ele tem uma lista de objetos que estão dentro do mundo.

Essa lista contém classes do tipo: ObjetoDoMundo

maxX é equivalente à dimensoes['x']
maxY é equivalente à dimensoes['y']
"""

import random
from typing import List, AnyStr
import utilidades
from classes.ObjetoDoMundo import ObjetoDoMundo


class Mundo:

    # dimensões
    maxX: int  # comprimento
    maxY: int  # altura

    # items no mundo
    items: List[ObjetoDoMundo] = []

    def __init__(self, x, y):
        self.maxX = x
        self.maxY = y

    def comprimento(self):
        return self.maxX

    def profundidade(self):
        return self.maxY

    def adicionaObjeto(self, objeto: ObjetoDoMundo):
        # gera id aleatório
        id = str(random.randint(1, 1000000))

        objeto.id = id
        self.items.append(objeto)

        return objeto

    def removeObjeto(self, objeto: ObjetoDoMundo):
        _, index = self.getItem(objeto)  # type: ignore
        if index:
            self.items.pop(index)

    def getItem(self, objeto: ObjetoDoMundo):
        for index, item in enumerate(self.items):
            if item.id == objeto.id:
                return item, index
        return None, None

    def getItemPorSimbolo(self, simbolo:AnyStr):
        items:List[ObjetoDoMundo] = []
        for _, item in enumerate(self.items):
            if item.objeto.simbolo == simbolo:
                items.append(item)
        return items

    def moveObjeto(self, objeto: ObjetoDoMundo, x: int, y: int):
        objetoAchado, _ = self.getItem(objeto)
        if objetoAchado == None:
            return False

        # checar se já existem items no mesmo lugar
        itemNaPosicao = self.getObjetosEmPosicao(x, y)
        if len(itemNaPosicao) > 0:
            self.onContatoNaMesmaPosicao(x, y, objeto)
        objetoAchado.x = x
        objetoAchado.y = y

        return True

    def onContatoNaMesmaPosicao(self, x: int, y: int, objeto: ObjetoDoMundo):
        items = self.getObjetosEmPosicao(x, y)
        for item in items:
            if item.id != objeto.id:
                self.removeObjeto(item)

        return True  # False se não puder mover

    def getObjetosEmPosicao(self, x: int, y: int):
        items: List[ObjetoDoMundo] = []
        for item in self.items:
            if item.x == x and item.y == y:
                items.append(item)
        return items

    def geraInstrucoes(self):
        instrucoes = {}
        for item in self.items:
            instrucoes[utilidades.geraCoordenada(
                item.x, item.y)] = item.objeto.simbolo
        return instrucoes

    def getItens(self):
        return self.items
