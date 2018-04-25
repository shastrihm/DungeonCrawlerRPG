from monster import *
from item import *
import os
import time
import updater
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.name = None
        self.location = None
        self.items = []

        self.fullHealth = 20
        self.health = self.fullHealth
        self.attack = 10
        self.defense = 17

        self.weaponEquip = None
        self.armorEquip = None

        self.expCap = 25
        self.exp = 0

        self.alive = True
        self.inCombat = False

        updater.register(self)

    def goDirection(self, direction):
        if self.location.getDestination(direction).level <= self.location.level: 
            self.location = self.location.getDestination(direction)
            return True
        else:
            success = False
            for key in self.items:
                if key.openlevel == self.location.getDestination(direction).level:
                    print()
                    print("Would you like to unlock this door? <<Yes/No>>")
                    answer = input()
                    if answer == "Yes":
                        key.unlock()
                        time.sleep(2)
                        success = True
                        self.location = self.location.getDestination(direction)
                        return True
                        break
            if not success:
                print()
                print("You need a key to unlock this door.")
                print()
                return False

    def pickup(self, item):
        print("You picked up " + item.name + ".")
        self.items.append(item)
        item.loc = self
        self.location.removeItem(item)

    def loot(self,item):
        #The same as pickup without removing the item from the location, since it
        #is for monster drops.
        print()
        print("You looted " + item.name + ".")
        print()
        self.items.append(item)
        item.loc = self

    def showInventory(self):
        clear()
        #item stacking
        stackedItems = stack(self.items)
        print("You are currently carrying:")
        print()
        for i in stackedItems:
            print(i + " x" + str(stackedItems[i]))
        print()
        inspect = input()

        try:
            if inspect.split()[0].lower() == "inspect":
                target = inspect[8:]
                for i in self.items:
                    if target.lower() == i.name.lower():
                        print(i.desc)
                        break
                print()
                input("Press enter to continue...")

            elif inspect.split()[0].lower() == "equip":
                target = inspect[6:]
                for i in self.items:
                    if target.lower() == i.name.lower():
                        try:
                            self.equipWeapon(i)
                        except AttributeError:
                            self.equipArmor(i)

            elif inspect.split()[0].lower() == "use":
                use_success = False
                target = inspect[4:]
                for i in self.items:
                    if target.lower() == i.name.lower():
                        try:
                            print("Consuming " + i.name + "...")
                            time.sleep(1.5)
                            i.consume(self)
                            use_success = True
                        except AttributeError:
                            print("You can't use that item now!")
                            use_success = True
                        input("Press enter to continue...")
                        break
                if not use_success:
                    print("You don't have that item!")
                    input("Press enter to continue...")

            else:
                input("Press enter to continue...")

        except IndexError: 
            input("Press enter to continue...")
    
    def showSummary(self):
        #me command
        clear()
        print("---Player: " + self.name + "---")
        print("Health: " + str(self.health)+'/'+str(self.fullHealth))
        print("Attack: " + str(self.attack))
        print("Defense: " + str(self.defense))
        print("Carrying " + str(len(self.items))+ " item(s).")
        if self.weaponEquip is not None:
            print("Wielding " + self.weaponEquip.name +".")
        else:
            print("Wielding no weapon")
        if self.armorEquip is not None:
            print("Wearing " + self.armorEquip.name + ".")
        else:
            print("Wearing no armor")
        print("EXP: " + str(self.exp))
        print("EXP until Level Up: " + str(self.expCap-self.exp))
        print()
        input("Press enter to continue...")
    
    def attackMonster(self, mon):
        #attack repertoire for player.
        clear()
        print("You are attacking " + mon.name)
        print()
        print("Your health is " + str(self.health) + ".")
        print(mon.name + "'s health is " + str(mon.health) + ".")
        print()
        
        damageDone = damage(self,mon)
        mon.health -= damageDone
        print("You dealt " + str(damageDone) + " damage.")
        if mon.health<=0:
            print(mon.name + " has been vanquished!")
            mon.grantXP(self)
            mon.alive = False
            if self.exp>= self.expCap:
                self.levelUp()
            mon.drop(self)
            mon.die()

            
        else:
            print(mon.name + " has " + str(mon.health) + " health remaining.")

        if self.health<=0:
            print("You died.")
            self.alive = False

        print()
        input("Press enter to continue...\n")

    def levelUp(self):
        #This is what happens when you level up. Stats increase by a random
        #but reasonable amount.
        hp_inc = random.randint(int(self.health//1.325),int(self.health)) 
        att_inc = abs(random.randint(self.attack-5,self.attack))
        def_inc = abs(random.randint(self.defense-5,self.defense))

        self.fullHealth += hp_inc
        self.attack += att_inc
        self.defense += def_inc
        print()
        print("Well done, brave " + self.name + ". You leveled up.")
        print("Your health capacity has been increased by " + str(hp_inc) + " to " + str(self.fullHealth) + ".")
        print("Your attack has been increased by " + str(att_inc) + " to " + str(self.attack) + ".")
        print("Your defense has been increased by " + str(def_inc) + " to " + str(self.defense) + ".")
        print()
        input("Press enter to continue...")
        #Then your exp resets and your expcap increases. 
        self.exp = 0
        self.expCap *= 1.5
        self.expCap = int(self.expCap)

    def update(self):
        #regeneration
        if self.health+5<=self.fullHealth:
            self.health+=5

        elif self.health<self.fullHealth:
            self.health+=1

    def equipArmor(self,armor):
        #Equips armor.
        if self.armorEquip is not None:
            self.defense -= self.armorEquip.defBonus

        self.armorEquip = armor
        self.defense += armor.defBonus
        print("Putting on...")
        time.sleep(1.5)
        print("Now wearing " + armor.name + ".")
        time.sleep(2)
        
    def equipWeapon(self,weapon):
        #Equips weapon
        if self.weaponEquip is not None:
            self.attack -= self.weaponEquip.attackBonus

        self.weaponEquip = weapon
        self.attack += weapon.attackBonus
        print("Getting used to the weight...")
        time.sleep(1.5)
        print("Now wielding " + weapon.name + "!")
        time.sleep(2)





class Medic:
    #NPC Medic class.
    def __init__(self, level, room):
        self.name = "Paul the Polite Priest"
        self.level = level
        self.room = room
        self.room.addNPC(self)
    def dialogue(self,towho):
        #My attempt at being witty.
        clear()
        print(self.name+ ": Psst... I'm actually on your side. Do you want to be healed? <<Yay or Nay?>>")
        answer = input()
        print()
        if answer.lower()=="yay":
            self.heal(towho)
            print()
            print(self.name+ ": There you go brave one. Safe travels!")
            print()
            input("Press enter to continue...")
        else:
            print()
            print(self.name+": That's too bad. I ought to not waste these bandages on these cursed pieces.")
            print(self.name+": Anyway you know where to find me, brave one.")
            print()
            input("Press enter to continue...")
    def heal(self,player):
        #Heals the player 
        healedBy = player.fullHealth-player.health
        player.health = player.fullHealth
        print()
        print("You have been healed by " + str(healedBy) + " points.")

class Promoter:
    #NPC Gatekeeper at the very end of the game
    def __init__(self,room):
        self.name = "Gatekeeper"
        self.room = room
        self.room.addNPC(self)

    def dialogue(self,towho):
        #Another attempt at being witty
        clear()
        print(self.name+ ": Congratulations, brave " + towho.name + ".")
        print("You have reached the depths of this dungeon.")
        print("Would you like a reward? <<yes/no>>")
        #Trick question.
        answer = input()
        print()
        if answer.lower() == "yes":
            print(self.name + ": FOOL! You shall be punished for your greed.")
            self.kill(towho)
        else:
            print(self.name + ": You are wise and not greedy. Congratulations, you have succeeded in your quest.")
            print()
            print("GAME OVER")
            time.sleep(1.5)
            sys.exit()

    def kill(self,player):
        #Brutally kills the player.
        print(self.name + " has wounded you by " + str(player.health) + " points.")
        print("You have died.")
        player.alive = False


def damage(committer, recipient):
    #damage formula
    return int(((committer.attack)**2)/((committer.attack)+(recipient.defense)))

def stack(items):
    #Counts the number of each item in your inventory. Called in player.showInventory
    names = [item.name for item in items]
    count = {}
    for i in names:
        if i in count:
          count[i]+=1
        else:
          count[i] = 1
    return count  