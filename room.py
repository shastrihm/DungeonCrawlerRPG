import random
import math
from monster import *
from player import *
from item import *

class Room:
    def __init__(self, description, level):
        self.desc = description
        self.abbrev = description.split()[1] + ' '+ description.split()[2]
        self.level = level
         #8 levels. each level has 8 rooms. This attribute is to facilitate 
         #interactions between levels. 
        self.monsters = []
        self.exits = []
        self.items = []
        self.NPCs = []
    def addExit(self, exitName, destination):
        self.exits.append([exitName, destination])
    def getDestination(self, direction):
        for e in self.exits:
            if e[0].split()[2]+' '+e[0].split()[3] == direction:
                return e[1]
    def connectRooms(room1, dir1, room2, dir2):
        #creates "dir1" exit from room1 to room2 and vice versa
        room1.addExit(dir1, room2)
        room2.addExit(dir2, room1)
    def exitNames(self):
        return [x[0] for x in self.exits]
    def destinationNames(self):
        return [x[1] for x in self.exits]
    def addNPC(self, NPC):
        self.NPCs.append(NPC)
    def addItem(self, item):
        self.items.append(item)
    def removeItem(self, item):
        self.items.remove(item)
    def addMonster(self, monster):
        self.monsters.append(monster)
    def removeMonster(self, monster):
        self.monsters.remove(monster)
    def hasItems(self):
        return self.items != []
    def hasNPCs(self):
        return self.NPCs != []
    def getItemByName(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False
    def hasMonsters(self):
        return self.monsters != []
    def getMonsterByName(self, name):
        for i in self.monsters:
            if i.name.lower() == name.lower():
                return i
        return False
    def getNPCByName(self,name):
        for i in self.NPCs:
            if i.name.lower() == name.lower():
                return i
        return False
    def randomNeighbor(self):
        return random.choice(self.exits)[1]




def randomlyGenerateMap():
    #Generates a map of 8 levels, each level has 8 rooms, except for the last two,
    #which are boss battles. 
    #init room and level names
    romNums = ['','I','II','III','IV','V','VI','VII','VIII']

    r1 = "Weapons Armory " #start out 
    r2 = "Knight's Stables " 
    r3 = "Bishop's Altar " 
    r4 = "EnPrise Pub " 
    r5 = "Castle Doors "  
    r6 = "Castle Carpet "
    singler7 = "Queen's Bedroom " #Bossfight 1
    singler8 = "King's Throne "   #Final Boss 
    roomList = []

    #create base 2-D matrix/array of map w/o connections yet
    for i in range(1,9): 
        roomList.append(Room(r1+romNums[i],1)) #index 0 to 7
    for i in range(1,9):
        roomList.append(Room(r2+romNums[i],2)) #index 8 to 15
    for i in range(1,9):
        roomList.append(Room(r3+romNums[i],3)) #index 16 to 23
    for i in range(1,9):
        roomList.append(Room(r4+romNums[i],4)) #index 24 to 31
    for i in range(1,9):
        roomList.append(Room(r5+romNums[i],5)) #index 32 to 39 
    for i in range(1,9):
        roomList.append(Room(r6+romNums[i],6)) #index 40 to 47
    
    roomList.append(Room(singler7+"X",7))          #index 48
    roomList.append(Room(singler8+"X",8))          #index 49


    indexMatrix = [[0,7],[8,15],[16,23],[24,31],[32,39],[40,47]] #[48,48],[49,49]

    #randomly choose room connections WITHIN each level
    def randomizeConnections(index1,index2):
        dirs = [["north","south"],["east","west"]]

        for i in range(index1,index2+1): #make sure each room has at least 1 edge (can be more)
            if len(roomList[i].exits) <4:
                n=i
                while n==i or roomList[n] in roomList[i].destinationNames():#no duplicates
                    n = random.randint(index1,index2)
                room1 = roomList[i]
                room2 = roomList[n]
                
                if random.uniform(0,1) < 0.5: #"randomly" assign direction
                    dir1 = dirs[0][0] + ", to " + room2.abbrev
                    dir2 = dirs[0][1] + ", to " + room1.abbrev
                else:
                    dir1 = dirs[1][0] + ", to " + room2.abbrev
                    dir2 = dirs[1][1] + ", to " + room1.abbrev

                
                Room.connectRooms(room1,dir1,room2,dir2)

        for i in range(0,2): #randomly assign 2 rooms with more edges. Max # of edges is 4.
            
            n=i
            m=i
            while n==m  or roomList[n] in roomList[m].destinationNames():#no duplicates
                n = random.randint(index1,index2)
                m = random.randint(index1,index2)
            room1 = roomList[m]
            room2 = roomList[n]

            if len(room1.exits)<4 and len(room2.exits)<4:
                if random.uniform(0,1) < 0.5: #"randomly" assign direction
                    dir1 = dirs[0][0] + ", to " + room2.abbrev
                    dir2 = dirs[0][1] + ", to " + room1.abbrev
                else:
                    dir1 = dirs[1][0] + ", to " + room2.abbrev
                    dir2 = dirs[1][1] + ", to " + room1.abbrev

                Room.connectRooms(room1,dir1,room2,dir2)

    for row in indexMatrix:
        randomizeConnections(row[0],row[1])

    def connectLevels(indexRange1,indexRange2): 
    #e.g. randomly connect the Weapons storerooms to the Knights stables, etc.
        a = indexRange1[0]
        b = indexRange1[1]
        c = indexRange2[0]
        d = indexRange2[1]

        n = random.randint(a,b)
        m = random.randint(c,d)
        while len(roomList[n].exits) >=4 and len(roomList[m].exits)>=4:
            n = random.randint(a,b)
            m = random.randint(c,d)
        room1 = roomList[n]
        room2 = roomList[m]

        Room.connectRooms(roomList[n],"north, to " + room2.abbrev,room2,"south, to "+room1.abbrev) #levels always top down unlike rooms

    for i in range(0,len(indexMatrix)-1):
        connectLevels(indexMatrix[i],indexMatrix[i+1])

    connectLevels(indexMatrix[-1],[48,48]) #connect castle carpet to bedroom
    connectLevels([48,48],[49,49]) #connect bedroom to throne (only 1 way)

    #run this piece of code to see the completed dungeon map!

    # for room in roomList:
    #       print()
    #       print(room.desc)
    #       for exita in room.exits:
    #         print(exita[0],exita[1].desc)

    return roomList


def randomlyDistributeMonsters(roomList):
    #distributes monsters within their respective levels (each level has different monsters)
    #Number of monsters per level is between 6 and 12, and they start at random locations

    #This list keeps track of the level indexes of the roomList
    im = [None,[0,7],[8,15],[16,23],[24,31],[32,39],[40,47]]

    #As the level increases, the monsters get harder (as evidenced by their increasing stats)
    #They also have different droptables (stronger monsters drop better gear)

    #Level 1 Armory
    numMons = random.randint(6,12)
    for i in range(numMons):
        room = random.randint(0,7)
        Pawn(name=None,health=10,room=roomList[room],attack=5,defense=2,dropTable=pawn_dropTable)

    #Level 2 Stables
    numMons = random.randint(6,12)
    for i in range(numMons):
        room = random.randint(8,15)
        Knight(name=None,health=20,room=roomList[room],attack=13,defense=10,dropTable=knight_dropTable)

    #Level 3 Altar
    numMons = random.randint(6,12)
    for i in range(numMons):
        room = random.randint(16,23)
        Bishop(name=None,health=30,room=roomList[room],attack=21,defense=18,dropTable=bishop_dropTable)

    #Level 4 Pub
    numMons = random.randint(6,12)
    for i in range(numMons):
        room = random.randint(24,31)
        Drunks(name=None,health=40,room=roomList[room],attack=29,defense=26,dropTable=drunk_dropTable)

    #Level 5 Doors
    numMons = random.randint(6,12)
    for i in range(numMons):
        room = random.randint(32,39)
        Rook(name=None,health=50,room=roomList[room],attack=37,defense=34,dropTable=rook_dropTable)

    #Level 6 Carpet
    numMons = random.randint(6,12)
    for i in range(numMons):
        room = random.randint(40,47)
        Scout(name=None,health=50,room=roomList[room],attack=45,defense=42,dropTable=scout_dropTable)

    #Level 7 Queen+King boss battle
    room = 48
    queen = Queen(name=None,health=100,room=roomList[room],attack=40,defense=60,dropTable=queen_dropTable)
    king = King(name=None,health=120,room=roomList[room],attack=60,defense=40,dropTable=king_dropTable)
    queen.ally = king
    king.ally = queen 

    #Level 8 Endgame 
    room = 49
    Promoter(room=roomList[room])

    # 1 medic per level
    for level in range(1,6+1):
        room = im[level][1]
        Medic(level=level,room=roomList[room])

def randomlyDistributeKeys(roomList):
    im = [None,[0,7],[8,15],[16,23],[24,31],[32,39],[40,47]]
    r1 = "Weapons Armory " #start out 
    r2 = "Knight's Stables " 
    r3 = "Bishop's Altar " 
    r4 = "EnPrise Pub " 
    r5 = "Castle Doors "  
    r6 = "Castle Carpet "
    singler7 = "Queen's Bedroom " #Bossfight 1
    singler8 = "King's Throne " 

    # 1 key per level. Each key gives the player access to the next level.
    # Their location in each level is random. 

    #Level 1 Armory
    room = random.randint(0,7)
    k1 = Key(name="Knight's Stables Key", desc=None, openWhichLevel=r2,openlevel=2)
    k1.putInRoom(roomList[room])

    #Level 2 
    room = random.randint(8,15)
    k2 = Key(name="Bishop's Altar Key", desc=None, openWhichLevel=r3,openlevel=3)
    k2.putInRoom(roomList[room])

    #Level 3 
    room = random.randint(16,23)
    k3 = Key(name="EnPrise Pub Key", desc=None, openWhichLevel=r4,openlevel=4)
    k3.putInRoom(roomList[room])

     #Level 4 
    room = random.randint(24,31)
    k4 = Key(name="Castle Doors Key", desc=None, openWhichLevel=r5,openlevel=5)
    k4.putInRoom(roomList[room])

     #Level 5 
    room = random.randint(32,39)
    k5 = Key(name="Castle Carpet Key", desc=None, openWhichLevel=r6,openlevel=6)
    k5.putInRoom(roomList[room])

     #Level 6 
    room = random.randint(40,47)
    k6 = Key(name="Queen's Bedroom Key", desc=None, openWhichLevel=singler7,openlevel=7)
    k6.putInRoom(roomList[room])

       #Level 7 
    room = 48
    k7 = Key(name="King's Throne Key", desc=None, openWhichLevel=singler8,openlevel=8)
    k7.putInRoom(roomList[room])



def showMapCurrentRoom(player):
    #Builds a map of the player's current room, with exits, keys, NPCs, and enemies
    #shown

    def mapLegend():
        #The legend
        e = 'E: enemy' + '\n'
        f = 'F: friendly' + '\n'
        k = 'K: door key' + '\n'
        a = '>,<,/\\, \/: exits' + '\n'
        return e+f+k+a

    def buildOutline(height,width):
        #builds a string of just the room outline with arrows as exits

        #counts how many exits in each direction
        nor_count, sou_count, eas_count, wes_count = 0,0,0,0
        for exit in player.location.exitNames():
            exitn = exit.split()[0]
            if exitn == "north,":
                nor_count+=1
            elif exitn == "south,":
                sou_count+=1
            elif exitn == "west,":
                wes_count+=1
            elif exitn == "east,":
                eas_count+=1

        lay1 = ' '+'-'*width + '\n'
        lay1list = list(lay1)
        offset_N = 3
        for N in range(0,nor_count):
            lay1list[offset_N] = '/'
            lay1list[offset_N+1] = '\\'
            offset_N+=6

        midlay = '|' + ' '*width + '|' + '\n'

        westArray = [] 
        for W in range(0,wes_count):
            westArray.append('<' + ' '*width + '|' + '\n')

        eastArray = [] 
        for E in range(0,eas_count):
            eastArray.append('|' + ' '*width + '>' + '\n')

        layh = ' '+'-'*width 
        layhlist = list(layh)
        offset_S = 3
        for S in range(0,sou_count):
            layhlist[offset_S] = '\\'
            layhlist[offset_S+1] = '/'
            offset_S+=6

        fixedHeight = height-(len(westArray)+len(eastArray))

        for i in range(0,fixedHeight):
            eastArray.append(midlay)

        midArray = eastArray + westArray
        random.shuffle(midArray)
        midBase1 = showMonsters(''.join(midArray))
        midBase2 = showNPCs(midBase1)
        midBase = showKeys(midBase2)
        base = ''.join(lay1list) + midBase + ''.join(layhlist)

        return base


    def showMonsters(base):
        #Shows monsters in the room's map
        enemy = len(player.location.monsters)
        baseList = list(base)
        for e in range(0,enemy):
            inHere = random.randint(0,len(baseList)-1)
            flag = False
            while not flag:
                if baseList[inHere] == ' ':
                    baseList[inHere] = 'E'
                    flag = True
                else:
                    inHere = random.randint(0,len(baseList)-1)
                    flag = False

        return ''.join(baseList)
        
    def showNPCs(base):
        #Shows NPCs in the room's map
        npc = len(player.location.NPCs)
        baseList= list(base)
        for n in range(0,npc):
            inHere = random.randint(0,len(baseList)-1)
            flag = False
            while not flag:
                if baseList[inHere] == ' ':
                    baseList[inHere] = 'F'
                    flag = True
                else:
                    inHere = random.randint(0,len(baseList)-1)
                    flag = False

        return ''.join(baseList)

    def showKeys(base):
        #Shows any keys in the room's map 
        key = len(player.location.items)
        baseList= list(base)
        for n in range(0,key):
            inHere = random.randint(0,len(baseList)-1)
            flag = False
            while not flag:
                if baseList[inHere] == ' ':
                    baseList[inHere] = 'K'
                    flag = True
                else:
                    inHere = random.randint(0,len(baseList)-1)
                    flag = False

        return ''.join(baseList)

    clear()
    base = buildOutline(20,40)
    print(player.location.desc)
    print(base)
    print()
    print('Legend: \n' + mapLegend())
    print()
    input('Press enter to continue...')    

    
