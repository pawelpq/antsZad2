import logging
SELF_PLAYER=1
ENEMS_PLAYER=2
MY_ANT = 0
ANTS = 0
DEAD = -1
LAND = -2
FOOD = -3
WATER = -4
class Utils:
    d={SELF_PLAYER:'1',ENEMS_PLAYER:'2',LAND:'.',WATER:'#'} 
    def __init__(self):
        pass
    def logInitInformationToStr(self,ants):
        
        t='=========== BASIC INFORMATION ================'
        t+='turns: '+str(ants.turns)
        t+='radiusAttac2: '+str(ants.attackradius2)
        t+='turntime: '+str(ants.turntime)
        t+='loadtime: '+str(ants.loadtime)
        t+='self ants: '+str(len(ants.my_ants()))
        t+='enems ants: '+str(len(ants.enemy_ants()))
        return t
    def calcMaxReward(self,listTerminalState):
        if len(listTerminalState)==0:
            return (-1,-1)
        (max,min)=(-1,-1)
        for state in listTerminalState:
            
            if max<state.reward[0]:
                max=state.reward[0]
            if min<state.reward[1]:
                min=state.reward[1]
        return (max,min)
    def getListBestTerminalState(self,listTerminalState,maxReward):
        temp=[]
        for state in listTerminalState:
            if state.reward==maxReward:
                temp.append(state)
        return temp
    def pathToList(self,terminalState):
        if terminalState==None:
            return None;
        pathList=[]
        while terminalState.parent!=None:
            pathList.append(terminalState)
            terminalState=terminalState.parent
        pathList.reverse()
        return pathList
    def pathToListPlusInitState(self,terminalState):
        if terminalState==None:
            return None;
        pathList=[]
        while terminalState!=None:
            pathList.append(terminalState)
            terminalState=terminalState.parent
        pathList.reverse()
        return pathList
    def getFirstBestState(self,listPath):
        d={}
        for path in listPath:
            if len(path)>=1:
                if d.get(path[1].dirs,-1)==-1:
                    d[path[1].dirs]=1
                else:
                    d[path[1].dirs]+=1
        bestMove=None
        lenBestMove=-1
        if len(d)>=1:
            bestMove=d
        for key in d.keys():
            if d[key]>lenBestMove:
                lenBestMove=d[key]
                bestMove=key
        for path in listPath:
            if path[0].dirs ==bestMove:
                return path[0]
        return None
    def getIndexTerminalBestList(self,terminalList,stateMap,nrTour):
        hashStateMap=hash(str(stateMap))
        
        i=0
        for listPath in terminalList:
           if len(listPath)>=(nrTour-1): 
               if hash(str(listPath[nrTour-1-1].map))==hashStateMap:
                   return i;
           i+=1
        return -1
    def listTerminalStateToListPath(self,listTerminalState):
        listPath=[]
        for bT in listTerminalState:
                listPath.append(self.pathToList(bT))
        return listPath
    def getNextState(self,terminalList,stateMap,nrTour):
        indexBestList=self.getIndexTerminalBestList(terminalList, stateMap, nrTour)
        logging.info(indexBestList)
        if(indexBestList==-1):
            logging.info('test')
            return None
        bestList=terminalList[indexBestList]
        newState=bestList[nrTour-1]
        if(newState!=None):
            return newState
        else:
            return None
    def getIndexCorrectDirection(self,ants,antLoc,state):
        if state==None:
            return -1
        for dir in state.dirs:
            if dir!='.':
                newLocAnt=ants.destination(antLoc,dir)
            else:
                newLocAnt=antLoc
            i=0
            for loc in state.loc:
                if loc==newLocAnt:
                    return i
                i+=1
        return -1
    def execCommand(self,ants,state,log=True):
        if state==None:
            if log:
                logging.info('Exec move: NO')
        for ant in ants.my_ants():
            indexDir=self.getIndexCorrectDirection(ants, ant, state)
            if indexDir>-1:
                command=state.dirs[indexDir]
                if command!='.':
                        ants.issue_order((ant,command))
            else:
                if log:
                    logging.info('Exec move: NO')
        if log:
            logging.info("Exec move: YES. Dirs: "+str(state.dirs))
      
               
            