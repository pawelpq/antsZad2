'''
Created on 15-05-2013
port
@author: Pawel
'''
import ants
from GameState import GameState
from StoreMovePosition import StoreMovePosition
import copy,logging, math,time
from timeit import itertools
SELF_PLAYER=1
ENEMS_PLAYER=2
MY_ANT = 0
ANTS = 0
DEAD = -1
LAND = -2
FOOD = -3
WATER = -4
d={SELF_PLAYER:'1',ENEMS_PLAYER:'2',LAND:'.',WATER:'#'}

class AntsGameSimulator:
    map=None
    movePosition=None
    rows=0
    cols=0
    attackradius=0
    offsets_cache={}
    initState=None
    storeMovePosition=None
    def __init__(self,ants):
        self.rows=ants.rows
        self.cols=ants.cols
        self.attackradius=ants.attackradius2
        self.storeMovePosition=StoreMovePosition(ants)
    def getInitState(self,ants,player):
        map=self.copyAndChangeMap(ants)
        state=GameState(map, player)
        self.saveSumDistance(state)
        self.initState=state
        return state
    def copyAndChangeMap(self,ants):
        map=ants.map
        for (r,c) in ants.my_ants():
            map[r][c]=SELF_PLAYER
        for ((r,c),nr) in ants.enemy_ants():
            map[r][c]=ENEMS_PLAYER
        return map
    def distanceManchatan2(self,row1,col1,row2,col2):
        d_col = min(abs(col1 - col2), self.cols - abs(col1 - col2))
        d_row = min(abs(row1 - row2), self.rows - abs(row1 - row2))
        return (d_col**2+d_row**2)
    def distanceEuclides2(self,row1,col1,row2,col2):
        d_col = (col1 - col2)
        d_row = (row1 - row2)
        return (d_col**2+d_row**2)
    def getAnts(self,state,player):
        list=[] 
        if player==ENEMS_PLAYER+SELF_PLAYER:
            for r in range(self.rows):
                for c in range(self.cols):
                    if state.map[r][c]>0:
                        list.append((r,c,state.map[r][c]))
        else:
            for r in range(self.rows):
                for c in range(self.cols):
                    if state.map[r][c]==player:
                        list.append((r,c,player))
        return list
    def destination(self, loc, d):
        """ Returns the location produced by offsetting loc by d """
        return ((loc[0] + d[0]) % self.rows, (loc[1] + d[1]) % self.cols)
    def neighbourhood_offsets(self, max_dist):
        """ Return a list of squares within a given distance of loc

            Loc is not included in the list
            For all squares returned: 0 < distance(loc,square) <= max_dist

            Offsets are calculated so that:
              -height <= row+offset_row < height (and similarly for col)
              negative indicies on self.map wrap thanks to python
        """
        if max_dist not in self.offsets_cache:
            offsets = []
            mx = int(math.sqrt(max_dist))
            for d_row in range(-mx,mx+1):
                for d_col in range(-mx,mx+1):
                    d = d_row**2 + d_col**2
                    if 0 < d <= max_dist:
                        offsets.append((
                            d_row%self.rows-self.rows,
                            d_col%self.cols-self.cols
                        ))
            self.offsets_cache[max_dist] = offsets
        return self.offsets_cache[max_dist]
    def nearby_ants(self,state, loc, max_dist, exclude=None):

        ants = []
        row, col = loc
        
        for d_row, d_col in self.neighbourhood_offsets(max_dist):
            p=state.map[row+d_row][col+d_col]
            if 0 <= p!=exclude:
                (r,c) = self.destination(loc, (d_row, d_col))
                ants.append((r,c,p))
        return ants
    def preKill(self,state):
        nearby_enemies = {}
        currentAnts=self.getAnts(state, ENEMS_PLAYER+SELF_PLAYER)
       
        for ant in currentAnts:
            r,c,p=ant
            if p==ENEMS_PLAYER:
                nearby_enemies[ant] = self.nearby_ants(state,(r,c), self.attackradius,ENEMS_PLAYER)
            else:
                nearby_enemies[ant] = self.nearby_ants(state,(r,c), self.attackradius,SELF_PLAYER)
        ants_to_kill = []
       
        for ant in currentAnts:
            # determine this ants weakness (1/power)
            weakness = len(nearby_enemies[ant])
            # an ant with no enemies nearby can't be attacked
            if weakness == 0:
                continue
            # determine the most powerful nearby enemy
            min_enemy_weakness = min(len(nearby_enemies[enemy]) for enemy in nearby_enemies[ant])
            # ant dies if it is weak as or weaker than an enemy weakness
            if min_enemy_weakness <= weakness:
                ants_to_kill.append(ant)
        return ants_to_kill
    def getMoveCombinationAll(self,player,state):
        posL=[]
        lD=[]
        for (r,c,p) in self.getAnts(state,player):
            locc,dir=self.storeMovePosition.getMove((r,c))
            posL.append(locc)
            lD.append(dir)
        return (list(itertools.product(*posL)),list(itertools.product(*lD)))
    def getClearMap(self,state,player):
        list = self.getAnts(state, player)
        
        map=copy.deepcopy(state.map)
        for (r,c,p) in list:
            map[r][c]=LAND
        return map
        
            
    def getNextStep(self,state):
        listState=[]
        st=time.time()
        if state.player==SELF_PLAYER:
            tmpPlayer=ENEMS_PLAYER
        else:
            tmpPlayer=SELF_PLAYER
        loc,dirs=self.getMoveCombinationAll(tmpPlayer, state)
     
        for i in range(len(loc)):
            tempLoc=loc[i]
            tempDirs=dirs[i]
            colisionMove=False
            for e in tempLoc:
                if tempLoc.count(e)>1:
                    colisionMove=True
            if colisionMove:
                continue
            cMap=self.getClearMap(state,tmpPlayer)
            for (r,c) in tempLoc:
                cMap[r][c]=tmpPlayer
            s=GameState(cMap, tmpPlayer)
            s.dirs=tempDirs
            listKill=self.preKill(s)
            for (r,c,p) in listKill:
                s.map[r][c]=LAND
            s.reward=(len(self.getAnts(s,SELF_PLAYER)),len(self.getAnts(s, ENEMS_PLAYER)))
            listState.append(s)
        
        return listState
    def testMoveCombination(self,player):
        l=[]
        for (r,c,p) in self.getAnts(player):
            l.append(self.storeMovePosition.getMove((r,c)))
       
            
    def testNeighbourhood_offsets(self):
        self.neighbourhood_offsets(3)
        logging.info(self.map[-1][-1])
        logging.info(self.preKill())
    def testNearby(self):
        self.map[1][1]=2
        self.currentAnts.append((1,1,2))
        l=self.preKill()
        logging.info(l)    
    
    
    def to_move(self, state):
        if state.player == SELF_PLAYER:
            return ENEMS_PLAYER
        else:
            return SELF_PLAYER
        
    def actions(self, state):
        listState=[]
        st=time.time()
        if state.player==SELF_PLAYER:
            tmpPlayer=ENEMS_PLAYER
        else:
            tmpPlayer=SELF_PLAYER
        loc,dirs=self.getMoveCombinationAll(tmpPlayer, state)
     
        for i in range(len(loc)):
            tempLoc=loc[i]
            tempDirs=dirs[i]
            colisionMove=False
            for e in tempLoc:
                if tempLoc.count(e)>1:
                    colisionMove=True
            if colisionMove:
                continue
            listState.append([tempLoc,tempDirs])
        return listState
    def terminal_test(self, state):
        return state.reward[0]==0 or state.reward[1]==0
    def utility(self,state,player):
        return state.reward[0]
    def saveSumDistance(self,state):
        sumMan2=0
        sumEuk2=0
        for (eR,eC,eP) in self.getAnts(state, ENEMS_PLAYER):
            for (sR,sC,sP) in self.getAnts(state, SELF_PLAYER):
                sumMan2+=self.distanceManchatan2(sR, sC, eR,eC)
                sumEuk2+=self.distanceEuclides2(sR, sC, eR,eC)
        state.sumDistManhattan2=sumMan2
        state.sumDistEuclides2=sumEuk2
    def result(self,state,a):
        [loc,dir]=a
        if state.player==SELF_PLAYER:
            tmpPlayer=ENEMS_PLAYER
        else:
            tmpPlayer=SELF_PLAYER
        cMap=self.getClearMap(state,tmpPlayer)
        for (r,c) in loc:
            cMap[r][c]=tmpPlayer
        s=GameState(cMap, tmpPlayer)
        s.dirs=dir
        s.loc=loc
        self.saveSumDistance(s)
        listKill=self.preKill(s)
      
        for (r,c,p) in listKill:
                s.map[r][c]=LAND
        s.reward=(len(self.getAnts(s,SELF_PLAYER)),len(self.getAnts(s, ENEMS_PLAYER)))
        
        return s
    def __str__(self):
        tmp = '\n'
        for row in self.map:
            tmp += '# %s\n' % ''.join([d[col] for col in row])
        return tmp
        