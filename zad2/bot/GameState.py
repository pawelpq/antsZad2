'''
Created on 16-05-2013

@author: Pawel
'''
SELF_PLAYER=1
ENEMS_PLAYER=2
MY_ANT = 0
ANTS = 0
DEAD = -1
LAND = -2
FOOD = -3
WATER = -4
class GameState:
    currentAnts=[]
    player=-1
    reward=[-1,-1]
    d={SELF_PLAYER:'1',ENEMS_PLAYER:'2',LAND:'.',WATER:'#'} 
    def __init__(self,map,player):
        self.map=map
        self.dirs=None
        self.player=player
        self.reward=(-1,-1)
        self.sumDistManhattan2=-1
        self.sumDistEuclides2=-1
        self.parent=None
        self.loc=None
    def __str__(self):
        mapTxt = '\n'
        for row in self.map:
            mapTxt += '# %s\n' % ''.join([self.d[col] for col in row])
        t='\n'
        t+='map\n: '+str(mapTxt)+'\n'
        t+='player: '+str(self.player)+'\n'
        t+='player: '+str(self.dirs)+'\n'
        t+='reward: '+str(self.reward)+'\n'
        t+="loc: "+str(self.loc)+'\n'
        t+='sum Man/Eul: '+str(self.sumDistManhattan2)+'/'+str(self.sumDistEuclides2)+'/n'
        return t
    def getHash(self):
        return hash(hash(str(self.map))+hash(str(self.dirs)))   