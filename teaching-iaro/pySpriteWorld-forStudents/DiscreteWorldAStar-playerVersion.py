# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys


# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def manhattan(x1,y1,x2,y2): #on calcule la distance de manhattan entre (x1,y1) et (x2,y2)
    return abs(x1 - x2) + abs(y1 - y2)

def frontH(tab,matriceH): #prend un tableau et renvoie les distances heuristiques de chaque position du tableau
    tabH = []
    j=0
    for i in tab:
        tabH.append(matriceH[tab[j][0]][tab[j][1]])
        j = j + 1 
    return tabH

class Noeud():
    def __init__(self,x,y,parent=None):
        self.parent = parent
        self.x = x
        self.y = y
        self.fils = []

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 1  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Building the matrix
    #-------------------------------
 
    #   00  0/Y
    #   X/0 X/Y
    
    #on cree une matrice nulle
    matriceH = np.zeros((21,21))
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
        
    
    #-------------------------------
    # Building the best path with A*
    #-------------------------------
    
    xGoal = goalStates[0][0] #row
    yGoal = goalStates[0][1] #col
    for x in range(0,21):
        for y in range(0,21):
            matriceH[x,y] = manhattan(x,y,xGoal,yGoal)
    row,col = initStates[0]
    f = [(row+1,col),(row-1,col),(row,col-1),(row,col+1)]
    fh = frontH(f,matriceH)
    while f != [] and (0 not in fh):
        choix = fh.index(min(fh))
        print(choix)
        fh.append(0)
        

    #-------------------------------
    # Moving along the path
    #-------------------------------
        
    # bon ici on fait juste un random walker pour exemple...
    
    row,col = initStates[0]
    #row2,col2 = (5,5)

    for i in range(iterations):
    
        # si on a  trouvé l'objet on le ramasse
        if (row,col)==goalStates[0]:
            o = game.player.ramasse(game.layers)
            game.mainiteration()
            print ("Objet trouvé!", o)
            break
        
        x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        next_row = row+x_inc
        next_col = col+y_inc
        if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=20 and next_col>=0 and next_col<=20:
            player.set_rowcol(next_row,next_col)
            print ("pos 1:",next_row,next_col)
            game.mainiteration()

            col=next_col
            row=next_row

            
        
            
        
        '''
        #x,y = game.player.get_pos()
    
        '''

    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()




