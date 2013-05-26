#!/usr/bin/env python
from ants import *
# Simple guardian bot - bouncing left and right
import logging
import itertools
from AntsGameSimulator import AntsGameSimulator
from StoreMovePosition import StoreMovePosition
from TreeGame import TreeGame
from Utils import Utils
from scipy.stats.distributions import loggamma
class BBot:

    tmp = {}
    turn = 0
    firstMove=True
    nrTour=1
    nrLevel=2
    utils=None
    listPath=[]
    simulation=None
    def __init__(self):
        logging.basicConfig(filename='BBot.log',level=logging.DEBUG,filemode='w')
        logging.info("===========")
        logging.info("Bot B v0.1")
        logging.info("===========")
        self.utils=Utils()   
    def do_setup(self,ants):
        pass
    def do_turn(self, ants):
        if self.firstMove:
             #boot init information
            t=self.utils.logInitInformationToStr(ants)
            logging.info(t)
            self.simulation=AntsGameSimulator(ants)
            s=self.simulation.getInitState(ants, 2)
            logging.info('======== INIT STATE ===========')
            logging.info(s)
            
            gameTree=TreeGame(self.simulation)
            timeout= (ants.loadtime/1000.0)-0.2
            t=gameTree.calculateTreeGame(s,timeout,10,True)
            logging.info('======== CALCULATE TREE ========')
            logging.info(t) 
            maxReward =self.utils.calcMaxReward(gameTree.listTerminal)  
            listBestTerm=self.utils.getListBestTerminalState(gameTree.listTerminal, maxReward)
            
            logging.info('maxReward: '+str(maxReward))
            logging.info('lenght listBestTerm: '+str(len(listBestTerm)))
                    
            self.listPath=[]
            for bT in listBestTerm:
                        self.listPath.append(self.utils.pathToListPlusInitState(bT))
            bestState=self.utils.getNextState(self.listPath, self.simulation.copyAndChangeMap(ants),2)
            logging.info(bestState)
            logging.info('===========FIRST EXEC STATE: ===========')
            logging.info(bestState)
            if bestState==None:
                logging.info('Best state is none. Bot not solved task.')
            else:
                self.utils.execCommand(ants, bestState)
            
            logging.info("==============END FIRST STEP==================")
            self.firstMove=False
        else:    
            if(self.nrTour%2==1):
                logging.info('=============TOUR NR: '+str(self.nrTour)+'=============')
                bestState=self.utils.getNextState(self.listPath, self.simulation.copyAndChangeMap(ants),self.nrLevel)
                if bestState!=None:
                    logging.info('========== STATE =========')
                    logging.info(bestState)
                    self.utils.execCommand(ants, bestState)
                   
                else:
                    logging.info("state: NONE  - Calc game tree")
                    s=self.simulation.getInitState(ants, 2)
                    logging.info(s)  
                    m=TreeGame(self.simulation)
                    
                    t=m.calculateTreeGame(s,(ants.turntime/1000.0)-0.05,10,True)
                    logging.info('======== CALCULATE TREE ========')
                    logging.info(t) 
                    maxReward =self.utils.calcMaxReward(m.listTerminal)
                    listBestTerm=self.utils.getListBestTerminalState(m.listTerminal, maxReward)
            
                    logging.info('maxReward: '+str(maxReward))
                    logging.info('lenght listBestTerm: '+str(len(listBestTerm)))
                    
                    self.listPath=[]
                    for bT in listBestTerm:
                        self.listPath.append(self.utils.pathToListPlusInitState(bT))
                    self.nrLevel=2
                    bestState=self.utils.getNextState(self.listPath, self.simulation.copyAndChangeMap(ants),self.nrLevel)
                    
                    logging.info('===========FIRST EXEC STATE: ===========')
                    logging.info(bestState)
            
                    if bestState==None:
                        logging.info('Best state is none. Bot not solved task.')
                    else:
                        self.utils.execCommand(ants, bestState)
                      
        self.nrTour+=1
        self.nrLevel+=1
if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    try:
        Ants.run(BBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
