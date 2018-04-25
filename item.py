import os
import time


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.loc = None
        self.openlevel = None
    def describe(self):
        clear()
        print(self.name)
        print(self.desc)
        print()
        input("Press enter to continue...")
    def putInRoom(self, room):
        self.loc = room
        room.addItem(self)

class Key(Item):
    #Keys open doors between levels. You cannot progress without them.
    def __init__(self,name,desc,openWhichLevel,openlevel):
        Item.__init__(self,name,desc)
        self.openWhichLevel = openWhichLevel #string description
        self.openlevel = openlevel #integer
        self.desc = "Unlocks the doors to " + str(self.openWhichLevel) + "."

    #Unlocks the door to the next level.
    def unlock(self):
        print()
        print("Unlocking...")
        time.sleep(3)
        print("Success! You unlocked " + str(self.openWhichLevel))
        print()

#all consumables need to have a consume method

class HealthPotion(Item):
    #Heals you by an amount (amount varies by type) and then dissappears.
    def __init__(self,name,desc,type,percent):
        Item.__init__(self,name,desc)
        self.percent = percent/100
        self.name = str(type) + " Health Potion"
        self.desc = "Restores your health by " + str(percent) + " percent."

    def consume(self,player):
        maxPotential = player.fullHealth*self.percent
        healedTo = player.health + maxPotential
        if healedTo >= player.fullHealth:
            player.health = player.fullHealth
            print()
            print("You were healed to full health.")
            print()
        elif healedTo < player.fullHealth:
            player.health+=healedTo
            print()
            print("You were healed to " + str(player.health) + " points.")

        player.items.remove(self)

#Allows you to escape a room that has enemies without killing the enemies.
#Transports you to a random neighboring room.
#Also lets you flee if you're in battle. Great for when you have low health.
class EscapeRope(Item):
    def __init__(self,name,desc):
        Item.__init__(self,name,desc)
        self.name = "Escape Rope"
        self.desc = "Allows you to bypass any enemies when leaving your current room. Moves you to a random neighboring room on consumption."

    def consume(self,player):
        room = player.location.randomNeighbor()
        while room.level > player.location.level:
            room = player.location.randomNeighbor()
        player.inCombat = False
        print("Throwing escape rope...")
        time.sleep(1)
        print("Landed at " + room.desc + "!")
        time.sleep(1.5)
        player.location = room
        player.items.remove(self)


#Weapons and Armor. They provide attack and defense bonuses.
class Weapon(Item):
    def __init__(self,name,desc,attackBonus):
        self.name=name
        self.desc=desc
        self.attackBonus = attackBonus

class Armor(Item):
    def __init__(self,name,desc,defBonus):
            self.name = name
            self.desc=desc
            self.defBonus = defBonus

#These are the 8 weapons and 8 armors. They have 'quirky' (my attempt at being
#quirky) names and descriptions based on actual chess players. 
weaponArray = [None,
              Weapon(name="Anderssen's Sword",desc="Adolf Anderssen's weapon of choice when tearing up 19th century German chess players. +1 attack",attackBonus=1),
              Weapon(name="Morphy's Metal Fork",desc="Paul Morphy's dinnertime favorite. +3 attack", attackBonus=3),
              Weapon(name="Euwe's Emu Knife", desc="Euwe would brandish one of these right before checkmate. +7 attack", attackBonus=7),
              Weapon(name="Alekhine's Wine Bottle", desc="Alekhine would throw this at you if he was losing. +5 attack", attackBonus=5),
              Weapon(name="Botvinnik's Botfly Blade", desc="One stab of this and the opponent turns to flies. +9 attack", attackBonus=9),
              Weapon(name="Karpov's Scythe", desc="Karpov liked his positions sharp. +11 attack", attackBonus=11),
              Weapon(name="Kramnik's Knife",desc="A truly deadly knife. +13 attack", attackBonus=13),
              Weapon(name="Carlsen",desc="Yes, you can use Magnus Carlsen as a weapon. +15 attack", attackBonus=15)]

armorArray = [None,
              Armor(name="Steinitz's Cloak",desc="A pretty moldy cloak. +1 defense", defBonus=1),
              Armor(name="Capablanca's Suit",desc="An ashy cloak predisposed to victory. +3 defense", defBonus=3),
              Armor(name="Lasker's Bathrobe",desc="Did Lasker wear a bathrobe? If he did, +5 defense", defBonus=5),
              Armor(name="Spassky's Earpiece",desc="Did the Russians cheat in 1972? If they did, +7 defense", defBonus=7),
              Armor(name="Fischer's Thin Skin", desc="The toughest thin skin. +9 defense", defBonus=9),
              Armor(name="Tal's Rolled Up Sleeves", desc="When you have these, game's over. +11 defense", defBonus=11),
              Armor(name="Anand's 90s Glasses", desc="For some reason Vishy Anand was unbreakable in these. +12 defense", defBonus=13),
              Armor(name="Kasparov",desc="Yes, you can use Garry Kasparov as armor. +15 defense", defBonus=15)]
              

#droptables for different monsters. Modeled as dictionaries with the keys being the item 
#object and the values being the probabilities of dropping.
pawn_dropTable = {HealthPotion(name=None,desc=None,type="Minor",percent=30): 0.50,
                  HealthPotion(name=None,desc=None,type="Greater",percent=50): 0.30,
                  HealthPotion(name=None,desc=None,type="Maximum",percent=100): 0.05,
                  EscapeRope(name=None,desc=None): 0.30,
                  weaponArray[1]: 0.20,
                  armorArray[1]: 0.20
                  }

knight_dropTable =   {HealthPotion(name=None,desc=None,type="Minor",percent=30): 0.40,
                      HealthPotion(name=None,desc=None,type="Greater",percent=50): 0.30,
                      HealthPotion(name=None,desc=None,type="Maximum",percent=100): 0.05,
                      EscapeRope(name=None,desc=None): 0.30,
                      weaponArray[2]: 0.20,
                      armorArray[2]: 0.20
                      }

bishop_dropTable =   {HealthPotion(name=None,desc=None,type="Minor",percent=30): 0.30,
                      HealthPotion(name=None,desc=None,type="Greater",percent=50): 0.30,
                      HealthPotion(name=None,desc=None,type="Maximum",percent=100): 0.10,
                      EscapeRope(name=None,desc=None): 0.30,
                      weaponArray[3]: 0.20,
                      armorArray[3]: 0.20
                      }

drunk_dropTable =   {HealthPotion(name=None,desc=None,type="Minor",percent=30): 0.30,
                    HealthPotion(name=None,desc=None,type="Greater",percent=50): 0.30,
                    HealthPotion(name=None,desc=None,type="Maximum",percent=100): 0.10,
                    EscapeRope(name=None,desc=None): 0.30,
                    weaponArray[4]: 0.20,
                    armorArray[4]: 0.20
                    }

rook_dropTable =   {HealthPotion(name=None,desc=None,type="Minor",percent=30): 0.30,
                    HealthPotion(name=None,desc=None,type="Greater",percent=50): 0.30,
                    HealthPotion(name=None,desc=None,type="Maximum",percent=100): 0.30,
                    EscapeRope(name=None,desc=None): 0.30,
                    weaponArray[5]: 0.20,
                    armorArray[5]: 0.20
                    }

scout_dropTable =   {HealthPotion(name=None,desc=None,type="Minor",percent=30): 0.20,
                    HealthPotion(name=None,desc=None,type="Greater",percent=50): 0.30,
                    HealthPotion(name=None,desc=None,type="Maximum",percent=100): 0.40,
                    EscapeRope(name=None,desc=None): 0.30,
                    weaponArray[6]: 0.20,
                    armorArray[6]: 0.20
                    }

queen_dropTable =   {HealthPotion(name=None,desc=None,type="Minor",percent=30): 0.05,
                    HealthPotion(name=None,desc=None,type="Greater",percent=50): 0.30,
                    HealthPotion(name=None,desc=None,type="Maximum",percent=100): 0.50,
                    EscapeRope(name=None,desc=None): 0.30,
                    weaponArray[7]: 1,
                    armorArray[7]: 1
                    }

king_dropTable =   {HealthPotion(name=None,desc=None,type="Minor",percent=30): 0.05,
                    HealthPotion(name=None,desc=None,type="Greater",percent=50): 0.30,
                    HealthPotion(name=None,desc=None,type="Maximum",percent=100): 0.30,
                    EscapeRope(name=None,desc=None): 0.30,
                    weaponArray[8]: 1,
                    armorArray[8]: 1
                    }


