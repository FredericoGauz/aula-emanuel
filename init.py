import sys

from classes.Mundo import Mundo
from classes.ObjetoDoMundo import ObjetoDoMundo
from classes.Game import Game
from classes.atores.atores import Bandido, Heroi

# CONSTANTES
comprimento = 10
largura = 10

# cria a classe Mundo
mundo = Mundo(comprimento, largura)

# adiciona personagens
# aqui é aonde podemos colocar aleatoriedade no jogo
mundo.adicionaObjeto(ObjetoDoMundo(Heroi('Emanuel'), 0, 0))
mundo.adicionaObjeto(ObjetoDoMundo(Bandido('El Cid'), 2, 2))
mundo.adicionaObjeto(ObjetoDoMundo(Bandido('El Raton'), 4, 6))

# cria a classe Game
game = Game(mundo)


# continuar o loop enquanto 'sair' for 'False'
def rodarTurnos(turno):
    sair = False
    while sair == False:
        turno, sair = game.turnoTotal(turno)


rodarTurnos(0)
# fim do jogo

repetir = input('Quer jogar novamente?')
if (repetir == 's'):
    print('Vamos lá!')
else:
    print('Até a proxima!')
    sys.exit()
