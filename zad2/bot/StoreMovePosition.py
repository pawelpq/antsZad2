'''
Created on 14-05-2013

@author: Pawel
'''
import logging

class StoreMovePosition:
    def __init__(self,ants):
        self.passibleDirection=['n','e','s','w','.']
        self.movePos={}
        self.moveDir={}
        self.generateMovePos(ants)
    def generateMovePos(self,ants):
        for r in range(ants.rows):
            for c in range(ants.cols):               
                if ants.passable((r,c)):
                    listMove=[]
                    listDir=[]
                    for dir in self.passibleDirection:
                        if dir!='.':
                            (tR,tC)=ants.destination((r,c),dir)
                            if ants.passable((tR,tC)):
                                listMove.append((tR,tC))
                                listDir.append(dir)
                        else:
                            listMove.append((r,c))
                            listDir.append('.')
                    self.movePos[(r,c)]=listMove
                    self.moveDir[(r,c)]=listDir
    def getMove(self,loc):
        return (self.movePos[loc],self.moveDir[loc])      