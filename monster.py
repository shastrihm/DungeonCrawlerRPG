import random
import updater
from player import *
from item import * 
import time

class Monster:
    def __init__(self, name, health, room, attack, defense, dropTable):
        self.name = name
        self.health = health
        self.attack = attack
        self.accuracy = 0.70
        self.defense = defense
        self.room = room
        self.alive = True

        self.dropTable = dropTable
        self.xpGain = None

        room.addMonster(self)
        updater.register(self)

    def update(self):
        #Since king and queen are bosses, they shall not move from room to room.
        filteredName = self.name.split()
        if filteredName[-1] != "Queen" and filteredName[-1] != "King":
            if random.random() < .5:
                self.moveTo(self.room.randomNeighbor())

    def moveTo(self, room):
        self.room.removeMonster(self)
        self.room = room
        room.addMonster(self)

    def drop(self,player):
        #Monsters can drop gear/potions/ropes. 
        #Probability of dropping something is based on their droptable, defined in item.py
        dropArray = []
        for item, rate in self.dropTable.items():
            if random.random() < rate:
                dropArray.append(item)
        print()
        if dropArray != []:
            print(self.name + " has dropped the following items:")
        
        commandSuccess = False

        while not commandSuccess and dropArray != []:
            for item in dropArray:
                print(item.name)
            print("Loot any of these items? <<Item name>> or <<no>> or <<all>>")
            answer = input()
            pickedUp = False
            if answer.lower() == "all":
                for item in dropArray:
                    player.loot(item)
                dropArray = []
                pickedUp = True
                commandSuccess = True
            elif answer.lower() == "no":
                commandSuccess = True
                break
            for item in dropArray:
                if answer.lower() == item.name.lower():
                    player.loot(item)
                    dropArray.remove(item)
                    pickedUp = True
            if not pickedUp:
                print()
                print("Keep dreaming. That item wasn't dropped.")
                print()
            

    def die(self):
        self.room.removeMonster(self)
        updater.deregister(self)

    def attackPlayer(self,player):
        #Monster's attacking repertoire
        if random.random() < self.accuracy:
            damageDone = damage(self,player)
            player.health -= damageDone
            print()
            print(str(self.name) + " attacked! You lost " + str(damageDone) + " health.")
            if player.health > 0:
                print("You have " + str(player.health) + " health remaining.")
        else:
            print()
            print(str(self.name)+" missed its attack!")

    def grantXP(self,player):
        #monster also grants a set amount of xp (different for different monsters)
        player.exp += self.xpGain
        print("You gained " + str(self.xpGain) + " exp.")


#Different monster classes obtain different stats on initialization in room.py
class Pawn(Monster):
    def __init__(self,name,health,room, attack, defense,dropTable):
        Monster.__init__(self,name,health,room,attack,defense,dropTable)
        adjectives = ['Pugnacious','Lowly','Wannabe-Queen','Totally Ordinary','Ambituous','Rusty']
        self.name = adjectives[random.randint(0,len(adjectives)-1)] + " Pawn"
        self.xpGain = 5

class Knight(Monster):
    def __init__(self,name,health,room, attack, defense,dropTable):
        Monster.__init__(self,name,health,room,attack,defense,dropTable)
        adjectives = ['Deranged','Rabid','Decorated','Heavily-Armed','Skeleton','Dark']
        self.name = adjectives[random.randint(0,len(adjectives)-1)] + " Knight"
        self.xpGain = 7

class Bishop(Monster):
     def __init__(self,name,health,room, attack, defense,dropTable):
        Monster.__init__(self,name,health,room,attack,defense,dropTable)
        adjectives = ['Fanatical','Orthodox','Extremist','Scientologist','Unlicensed','Progressive']
        self.name = adjectives[random.randint(0,len(adjectives)-1)] + " Bishop"
        self.xpGain = 9

class Drunks(Monster):
    def __init__(self,name,health,room, attack, defense,dropTable):
        Monster.__init__(self,name,health,room,attack,defense,dropTable)
        adjectives = ['24/7','Sober','First-Time','Rowdy','Underage','Violent']
        self.name = adjectives[random.randint(0,len(adjectives)-1)] + " Drunk"
        self.xpGain = 15

class Rook(Monster):
    def __init__(self,name,health,room, attack, defense,dropTable):
        Monster.__init__(self,name,health,room,attack,defense,dropTable)
        adjectives = ['Gated','Chained','Teetering','Sturdy','Brass','Granite']
        self.name = adjectives[random.randint(0,len(adjectives)-1)] + " Rook"
        self.xpGain = 20

class Scout(Monster):
    def __init__(self,name,health,room, attack, defense,dropTable):
        Monster.__init__(self,name,health,room,attack,defense,dropTable)
        adjectives = ['Nimble','Unsuspecting','Newly-Hired','Loyal','Double-Agent','Tipsy']
        self.name = adjectives[random.randint(0,len(adjectives)-1)] + " Scout"
        self.xpGain = 25


#Queen and King have different monster behaviour since they are bosses.
class Queen(Monster):
    def __init__(self,name,health,room, attack, defense,dropTable):
        Monster.__init__(self,name,health,room,attack,defense,dropTable)
        self.name = "Powerful and Magnificent Empress Queen"
        self.healthCap = 100
        self.xpGain = 100
        self.accuracy = 0.80
        self.ally = None

    def attackPlayer(self,player):
        if random.random() < self.accuracy:
            damageDone = damage(self,player)
            player.health -= damageDone
            print()
            print(str(self.name) + " attacked! You lost " + str(damageDone) + " health.")
            if player.health > 0:
                print("You have " + str(player.health) + " health remaining.")
            self.healAlly(self.ally)
        else:
            print()
            print(str(self.name)+" missed its attack!")
            self.healAlly(self.ally)

    # Can heal the King
    def healAlly(self,ally):
        if random.random() < 0.05:
            ally.health = ally.healthCap
            print()
            print(self.name + " healed " + self.ally.name + " to full health!")
        elif random.random() < 0.30 and ally.health+15 <=ally.healthCap:
            ally.health+=15
            print()
            print(self.name + " healed " + self.ally.name + " to " + str(self.ally.health) + " health!")
        elif random.random() < 0.50 and ally.health+10 <=ally.healthCap:
            ally.health+=10
            print()
            print(self.name + " healed " + self.ally.name + " to " + str(self.ally.health) + " health!")
        elif random.random() < 0.70 and ally.health+7 <=ally.healthCap:
            ally.health+=7
            print()
            print(self.name + " healed " + self.ally.name + " to " + str(self.ally.health) + " health!")



class King(Monster):
    def __init__(self,name,health,room, attack, defense,dropTable):
        Monster.__init__(self,name,health,room,attack,defense,dropTable)
        self.name = "The King"
        self.healthCap = 120
        self.xpGain = 200
        self.accuracy = 0.90
        self.ally = None

    def attackPlayer(self,player):
        if random.random() < self.accuracy:
            damageDone = damage(self,player)
            player.health -= damageDone
            print()
            print(str(self.name) + " attacked! You lost " + str(damageDone) + " health.")
            if player.health > 0:
                print("You have " + str(player.health) + " health remaining.")
            self.healAlly(self.ally)
        else:
            print()
            print(str(self.name)+" missed its attack!")
            self.healAlly(self.ally)

    # Can heal the Queen 
    def healAlly(self,ally):
        if random.random() < 0.05:
            ally.health = ally.healthCap
            print()
            print(self.name + " healed " + self.ally.name + " to full health!")
        elif random.random() < 0.30 and ally.health+15 <=ally.healthCap:
            ally.health+=15
            print()
            print(self.name + " healed " + self.ally.name + " to " + str(self.ally.health) + " health!")
        elif random.random() < 0.50 and ally.health+10 <=ally.healthCap:
            ally.health+=10
            print()
            print(self.name + " healed " + self.ally.name + " to " + str(self.ally.health) + " health!")
        elif random.random() < 0.70 and ally.health+7 <=ally.healthCap:
            ally.health+=7
            print()
            print(self.name + " healed " + self.ally.name + " to " + str(self.ally.health) + " health!")

#Damage formula
def damage(committer, recipient):
    return int(((committer.attack)**2)/((committer.attack)+(recipient.defense)))

#Turn based combat between monsters in room and player.
def combatSequence(monsterArray,player):
    player.inCombat = True
    while monsterArray != []: 
        clear() 
        for monster in monsterArray:
            monster.attackPlayer(player)

        if player.health <= 0:
            player.alive = False
            print("You died.")
            break

        print()
        print('~~ Enemies ~~')
        for i in monsterArray:
            print(i.name)
        print()
        print("Choose which enemy to attack...<<enemy name>> or <<random>>. Or use an item in your <<inventory>>.")
        attackThis = input()
        commandSuccess=False
        while player.inCombat and not commandSuccess:
            for i in monsterArray:
                if attackThis == i.name:
                    commandSuccess = True
                    player.attackMonster(i)
                    break
            if attackThis.lower() == "random":
                commandSuccess = True
                player.attackMonster(random.choice(monsterArray))
            elif attackThis.lower() == "inventory":
                commandSuccess = True
                player.showInventory()
            elif attackThis.lower() == "me":
                player.showSummary()
                commandSuccess = True
            if not commandSuccess:
                print("You're probably imagining that enemy. Pick again.")
                attackThis = input()

        if not player.inCombat:
            break

        for monster in monsterArray:
            if not monster.alive:
                monster.die()
                monsterArray.remove(monster)

#My attempt at being witty in a cutscene. As you can see I am not very witty.
def finalboss_dialogue(player):
    queen = "Powerful and Magnificent Empress Queen: "
    king = "The King: "
    you = player.name + ": "
    delay = 1.5
    print(queen + "zZzZzZ...")
    time.sleep(delay)
    print(king + "zzzzzzzzzz...")
    time.sleep(delay)
    print(queen + "...rrrrr....")
    time.sleep(delay)
    print(king + ".......")
    time.sleep(delay)
    print(queen + "Who... are you...")
    time.sleep(delay)
    print(you + "I'm not sure. I think I'm supposed to fight you guys?")
    time.sleep(delay)
    print(king + "Didn't you come last week to try and fight us....?")
    time.sleep(delay)
    print(queen + "...And failed?")
    time.sleep(delay)
    print(you + "No.")
    time.sleep(delay)
    print(king + "No as you you didn't fail? I'm pretty sure we so nimbly kicked you back to the Weapons Armory.")
    time.sleep(delay)
    print(you + "No, I didn't come last week. This is my first time, I think.")
    time.sleep(delay)
    print(queen + "Well then. How dare you come into this bedroom and demand to fight us.")
    time.sleep(delay)
    print(king + "Yes, how dare you.")
    time.sleep(delay)
    print(queen + "If you can defeat us, you are the best we've come across. But you can't.")
    time.sleep(delay)
    print(king + "Get ready.")
    print()
    input("Press enter to continue...")
    
