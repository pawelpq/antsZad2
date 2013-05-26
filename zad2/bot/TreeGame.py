import AntsGameSimulator 
import logging,time
from unittest.test.support import LoggingResult
from numpy.ma.core import logical_and
from cgi import log
class TreeGame:
    '''
    classdocs
    '''


    def __init__(self,gameSimulator):
        self.gameSimulator=gameSimulator
        
        self.listState=[]
        self.listTerminal=[]
        self.hashTable=[]
        self.nrLevel=0
        
    def testDistSelfEnem(self,state):
        pParentEuc2=state.parent.sumDistEuclides2
        pParentMan2=state.parent.sumDistManhattan2
        if(state.sumDistEuclides2<=pParentEuc2 or state.sumDistManhattan2<=pParentMan2):
            return True
        else:
            return False           
    def generateNextLevelTree(self,listStateParentLevel,st,timeout):
        tempList=[]
        for parentState in listStateParentLevel:
            for a in self.gameSimulator.actions(parentState):
                if ((time.time()-st)>timeout):
                    return []
                aChild=self.gameSimulator.result(parentState,a)
                aChild.parent=parentState
                if self.gameSimulator.terminal_test(aChild):
                    self.listTerminal.append(aChild)
                else:
                    if(self.getHash(aChild) in self.hashTable):
                        pass
                    else:
                        self.hashTable.append(self.getHash(aChild))
                        tempList.append(aChild)
        self.nrLevel+=1
        return tempList
    def getHash(self,state):
        return hash(hash(str(state.map))+hash(str(state.dirs)))   
    def calculateTreeGame(self,initState,timeout,depthMax,log=True):
        textLog='Calculate tree game\n'
        depth=0
        currentList=[]
        sumTime=0
        st=time.time()
        currentList=self.generateNextLevelTree([initState],timeout,st)
        depth+=1
        tempTime=time.time()-st
        sumTime+=tempTime
        textLog+='Level:'+str(self.nrLevel)+'\n timeGenLev: '+str(tempTime)+'\nsumTime: '+str(sumTime)+' \n'
        textLog+='Count level state: '+str(len(currentList))+'\n'
        textLog+='=====================\n'
        if(sumTime>=timeout):
            textLog+="timeout"
            if log:
                return textLog
            else:
                return ''
        while True:
            if depth>=depthMax:
                textLog+="Max Depth"
                break
            currentList=self.generateNextLevelTree(currentList,timeout,st)
            if currentList==[]:
                textLog+="timeout"
                break
            depth+=1
            tempTime=time.time()-st
            sumTime+=tempTime
            textLog+='Level:'+str(self.nrLevel)+'\n timeGenLev: '+str(tempTime)+'\nsumTime: '+str(sumTime)+' \n'
            textLog+='Count level state: '+str(len(currentList))+'\n'
            textLog+='Time: '+str(tempTime)+'\n'
            textLog+='Sum Time: '+str(sumTime)+'\n'
            textLog+='===================\n'
            
            if(sumTime>=timeout):
                textLog+="timeout"
                break
            if len(currentList)==0:
                break
        if log:
            return textLog
        else:
            return ''
    def getListMove(self):
        if len(self.listTerminal)==0:
            return []
        bestTemp=self.listTerminal[0]
        for e in self.listTerminal:
            if bestTemp.reward[0]<e.reward[0]:
                logging.info('ok')
                bestTemp=e;
        
        tempTerminalStateList=[]
        while bestTemp.parent!=None:
            
            tempTerminalStateList.append(bestTemp)
            bestTemp=bestTemp.parent
        tempTerminalStateList.reverse()
        return tempTerminalStateList
        