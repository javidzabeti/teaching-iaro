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
# ---- Main                ----
# ---- ---- ---- ---- ---- ----
def manhattan(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)

class Node:
    def __init__(self,x,y,dParcourue,dMan,parent=None):
        self.parent = parent
        self.dParcourue = dParcourue
        self.dMan = dMan
        self.x = x
        self.y = y

def ajouteFront(noeud,wallStates,xFiole,yFiole):
    l=[]
    if(((noeud.x+1,noeud.y) not in wallStates) and (noeud.x+1 >= 0) and (noeud.y >= 0) and (noeud.x+1 <= 19) and (noeud.y <= 19)):
        dMan = manhattan(noeud.x+1,noeud.y,xFiole,yFiole)
        l.append(Node(noeud.x+1,noeud.y,noeud.dParcourue+1,dMan,noeud))
    if(((noeud.x-1,noeud.y) not in wallStates) and (noeud.x-1 >= 0) and (noeud.y >= 0) and (noeud.x-1 <= 19) and (noeud.y <= 19)):
        dMan = manhattan(noeud.x-1,noeud.y,xFiole,yFiole)
        l.append(Node(noeud.x-1,noeud.y,noeud.dParcourue+1,dMan,noeud))
    if(((noeud.x,noeud.y+1) not in wallStates) and (noeud.x >= 0) and (noeud.y+1 >= 0) and (noeud.x <= 19) and (noeud.y+1 <= 19)):
        dMan = manhattan(noeud.x,noeud.y+1,xFiole,yFiole)
        l.append(Node(noeud.x,noeud.y+1,noeud.dParcourue+1,dMan,noeud))   
    if(((noeud.x,noeud.y-1) not in wallStates) and (noeud.x >= 0) and (noeud.y-1 >= 0) and (noeud.x <= 19) and (noeud.y-1 <= 19)):
        dMan = manhattan(noeud.x,noeud.y-1,xFiole,yFiole)
        l.append(Node(noeud.x,noeud.y-1,noeud.dParcourue+1,dMan,noeud))
    return l

def minMan(listNoeud):
    mini = listNoeud[0].dMan
    n = listNoeud[0]
    for i in listNoeud:
        if i.dMan < mini:
            n = i
            mini = i.dMan
    return n

def minParcourue(listNoeud,xFiole,yFiole):
    if listNoeud == []:
        return -1
    n = None
    for i in listNoeud:
        if ((i.x == xFiole) and (i.y == yFiole)):
            n = i
    if n == None:
        return -1
    if n.parent == None:
        return n
    nNext = n.parent
    while nNext.parent != None:
        n = nNext
        nNext = n.parent
    return n

def minPar(listNoeud):
    mini = listNoeud[0].dParcourue
    n = listNoeud[0]
    for i in listNoeud:
        if i.dParcourue < mini:
            n = i
            mini = i.dParcourue
    return n
    
def bestRowCol(posPlayer,posFiole,wallStates):
    xPlayer = posPlayer[0]
    yPlayer = posPlayer[1]
    xFiole = posFiole[0]
    yFiole = posFiole[1]
    front = []
    res = []
    res.append(Node(xPlayer,yPlayer,0,manhattan(xPlayer,yPlayer,xFiole,yFiole)))
    for i in ajouteFront(res[0],wallStates,xFiole,yFiole):
        front.append(i)
    test = True
    while front != []:
        noeudMin = minPar(front)
        res.append(noeudMin)
        front.remove(noeudMin)
        for i in ajouteFront(noeudMin,wallStates,xFiole,yFiole):
            for j in front:
                if test:
                    if((i.x == j.x) and (i.y == j.y)):
                        if i.dParcourue < j.dParcourue:
                            front.append(i)
                            front.remove(j)
                        test = False
            for j in res:
                if test:
                    if((i.x == j.x) and (i.y == j.y)):
                        if i.dParcourue < j.dParcourue:
                            res.append(i)
                            res.remove(j)
                        test = False
            if test:
                front.append(i)
            test = True
    n = minParcourue(res,xFiole,yFiole)
    if n == -1:
        return xPlayer,yPlayer
    return n.x,n.y

def nearestGoal(posPlayer,wallStates,goalStates):
    xPlayer = posPlayer[0]
    yPlayer = posPlayer[1]
    dist = 10000
    x=-1
    for e in range(0,len(goalStates)):
        xFiole = goalStates[e][0]
        yFiole = goalStates[e][1]
        front = []
        res = []
        res.append(Node(xPlayer,yPlayer,0,manhattan(xPlayer,yPlayer,xFiole,yFiole)))
        for i in ajouteFront(res[0],wallStates,xFiole,yFiole):
            front.append(i)
        test = True
        while front != []:
            noeudMin = minPar(front)
            res.append(noeudMin)
            front.remove(noeudMin)
            for i in ajouteFront(noeudMin,wallStates,xFiole,yFiole):
                for j in front:
                    if test:
                        if((i.x == j.x) and (i.y == j.y)):
                            if i.dParcourue < j.dParcourue:
                                front.append(i)
                                front.remove(j)
                            test = False
                for j in res:
                    if test:
                        if((i.x == j.x) and (i.y == j.y)):
                            if i.dParcourue < j.dParcourue:
                                res.append(i)
                                res.remove(j)
                            test = False
                if test:
                    front.append(i)
                test = True
        for k in res:
            if k.x == xFiole and k.y == yFiole:
                if k.dParcourue < dist:
                    dist = k.dParcourue
                    x = e
    return x

game = Game()

def init(_boardname=None):
    carte = ['cluedo','match','match2','pathfindingWorld3','pathfindingWorld_multiPlayer','pathfindingWorld_MultiPlayer2','pathfindingWorld_MultiPlayer3','pathfindingWorld_MultiPlayer4','thirst','tictactoe','tictactoeBis']
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'match'
    name = carte[1]
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 10  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 500 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    
    
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
       
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers
    
    
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
    # Placement aleatoire des fioles de couleur 
    #-------------------------------
    
    for o in game.layers['ramassable']: # les rouges puis jaunes puis bleues
    # et on met la fiole qqpart au hasard
        x = random.randint(1,19)
        y = random.randint(1,19)
        while (x,y) in wallStates:
            x = random.randint(1,19)
            y = random.randint(1,19)
        o.set_rowcol(x,y)
        game.layers['ramassable'].add(o)
        game.mainiteration()                

    print(game.layers['ramassable'])
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]

    
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
        
    # bon ici on fait juste plusieurs random walker pour exemple...
    
    posPlayers = initStates
    print(len(wallStates))
    oldRow = []
    oldCol = []
    for k in posPlayers:
        wallStates.append(k)
    for i in range(iterations):
        
        for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
            row,col = posPlayers[j]
            #x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
            #next_row = row+x_inc
            #next_col = col+y_inc
            goal = nearestGoal(posPlayers[j],wallStates,goalStates)
            next_row,next_col = bestRowCol(posPlayers[j],goalStates[goal],wallStates)
            # and ((next_row,next_col) not in posPlayers)
            if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19:
                players[j].set_rowcol(next_row,next_col)
                #print ("pos :", j, next_row,next_col)
                game.mainiteration()
                wallStates.remove((row,col))
                col=next_col
                row=next_row
                wallStates.append((row,col))
                posPlayers[j]=(row,col)
            
      
            # si on a  trouvé un objet on le ramasse
            if (row,col) in goalStates:
                o = players[j].ramasse(game.layers)
                game.mainiteration()
                #print ("Objet trouvé par le joueur ", j)
                goalStates.remove((row,col)) # on enlève ce goalState de la liste
                score[j]+=1
                
        
                # et on remet un même objet à un autre endroit
                x = random.randint(1,19)
                y = random.randint(1,19)
                while (x,y) in wallStates:
                    x = random.randint(1,19)
                    y = random.randint(1,19)
                o.set_rowcol(x,y)
                goalStates.append((x,y)) # on ajoute ce nouveau goalState
                game.layers['ramassable'].add(o)
                game.mainiteration()                
                
                break
            
    
    print ("scores:", score)
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


