from room import *
from player import *
from item import *
from monster import *
import os
import updater
import pickle
import time


def promptContinuation():
    #Asks the player if they want to load a saved game file
    print()
    print("Load previously saved game file... <<yes>> or <<no>>?")
    answer = input()
    return answer.lower() == "yes"

def gameLoreIntro():
    #My attempt at being witty... yet again...
    delay = 2
    print("You are just a pawn...")
    print()
    time.sleep(delay)
    print("Placed on this chessboard by the Queen and King to win glory...")
    print()
    time.sleep(delay)
    print("Or to perish... yeah, that makes more sense...")
    print()
    time.sleep(delay)
    print("You're can't feel anything in the dark... Here, take this torch.")
    print()
    time.sleep(delay)
    print("You're in the Weapon's Armory right now. Pawns hustle and bustle to keep track of the kingdom's weapons...")
    print()
    time.sleep(delay)
    print("Then there's the raucous Knight's Stables... All the valiant Knights who defend the kingdom feed their horses here...")
    print()
    time.sleep(delay)
    print("The loudness of the stables is succeeded by the silence of the Bishop's Altar... It's usually empty except for the actual bishops... wierd lot...")
    print()
    time.sleep(delay)
    print("And then oddly enough, the quietness of the altar is succeeded by the drunks in the EnPrise Pub. One step in there and you'll pass out from the alcohol...")
    print()
    time.sleep(delay)
    print("Then you get into the castle proper. The Castle Doors are home to the watchful rooks...")
    print()
    time.sleep(delay)
    print("An almost endless pathway then awaits... the Castle Carpet will fool you with lightning quick scouts watching your every move...")
    print()
    time.sleep(delay)
    print("Then you will find the Queen's Bedroom... if you are lucky. The Queen and King will not like you intruding, and they will assault you...")
    print()
    time.sleep(delay)
    print("Your mission is to defeat them and meet the gatekeeper. From there, only time will tell...")
    print()
    time.sleep(delay)
    print()
    input("Press enter to continue...")

def gameIntro():
    clear()
    gameLoreIntro()
    #Pattern intro with game name, hook
    clear()
    print("""
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          ~~~~~~~~~~~~~~~~~~TRAPPED IN THE CHESSBOARD~~~~~~~~~~~~~~~~~~~
          ~~~~~~~~~~~~~~~A dungeon-crawler RPG by Hrishee~~~~~~~~~~~~~~~
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          ~~~~~~~~~~~~~~~~~~~~~ YOU'RE ONLY A PAWN ~~~~~~~~~~~~~~~~~~~~~
          ~~~~~~~~~~~~~~~~ AND YOU WILL ALWAYS BE A PAWN ~~~~~~~~~~~~~~~
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          """)
    
    print()
    print("What is your name, hero?")
    name = input()
    player.name = name
    print()
    print("Welcome, brave " + name + ". A mighty challenge awaits.")
    input('<<Press enter to play>>')
    showHelp()
    

def createWorld():
    #randomly generates the world (rooms,items,monsters) with functions in room.py
    mapd = randomlyGenerateMap()
    player.location = mapd[0] #start Weapons Storeroom I
    randomlyDistributeMonsters(mapd)
    randomlyDistributeKeys(mapd)
    return mapd

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def printSituation():
    #Prints the current status of the player's room 
    clear()
    print(player.location.desc)
    print()

    if player.location.hasMonsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m.name)
        print()

    if player.location.hasItems():
        print("This room contains the following items:")
        for i in player.location.items:
            print(i.name)
        print()

    if player.location.hasNPCs():
        print("This room contains the following NPCs:")
        for n in player.location.NPCs:
            print(n.name)
        print()

    print("You can go in the following directions:")
    for e in player.location.exitNames():
        print(e)
    print()
    print("type <<help>> for help.")
    print()

def showHelp():
    #Help Menu. Very useful commands!
    clear()
    print("me -- shows a summary of your current status")
    print("save -- saves the game into a file so you can exit out of the game and return to it later.")
    print("go <abbrev> -- moves you to that room. (e.g. 'go Armory III')")
    print("inventory -- opens your inventory")
    print("inspect <item name> -- gives a description of the item. Use in world if target item is in world, otherwise use in inventory if you already have the item.")
    print("use <item name> -- while in inventory, consumes the item. Fails if the item is not a consumable.")
    print("equip <weapon/armor name> -- while in inventory, equips the weapon or armor of choice.")
    print("attack -- ensues combat sequence with all enemies in the current room")
    print("pickup <item> -- picks up the item in world. Not during monster drops.")
    print("talk <NPC> -- interact with NPC")
    print("map -- shows a map of your current room, including exits, enemies, NPCs, and items")
    print("exit -- exits out of the game")
    print("help -- shows the help menu")
    print()
    input("Press enter to continue...")

def saveGame():
    #save game. Write player and world objects to .dat file.
    with open("savedgamefile.dat", "wb") as f:
        pickle.dump([player,mapd], f, protocol=2)
        
def loadGame():
    #load game file. Retrieves player and world objects from .dat file.
    with open("savedgamefile.dat", "rb") as f:
        [player, mapd] = pickle.load(f)
        return [player,mapd]

loadedGame = False
if promptContinuation():
    #Tries to load game. If no save file, just restarts game.
    try:
        player = loadGame()[0]
        mapd = loadGame()[1]
        loadedGame = True
    except FileNotFoundError:
        print()
        print("No saved game file found. Starting game from beggining...")
        time.sleep(2.3)

if not loadedGame:
    player = Player()
    gameIntro()
    mapd = createWorld()

playing = True
while playing and player.alive:
    printSituation()
    commandSuccess = False
    timePasses = False
    while not commandSuccess:
        commandSuccess = True
        command = input("<<What now? >> ")
        if command == '': #player didn't input anything
            print()
            print("Try doing something next time.")
            print()
            commandSuccess = False
        
        commandWords = command.split()
        if commandWords != []:

            if commandWords[0].lower() == "go":   #can handle multi word directions.
                try:
                    if player.location.hasMonsters():
                        print('There are enemies blocking the exit. You shall not pass.')
                        commandSuccess = False
                    else:
                        test = player.goDirection(commandWords[1]+' '+commandWords[2]) #go Armory VI
                        if not test:
                            commandSuccess = False
                        else:
                            timePasses = True
                except (AttributeError,IndexError) as e:
                    print()
                    print("You can't go to that room!")
                    print()
                    commandSuccess = False

                # player.goDirection(commandWords[1]+' '+commandWords[2]) #go Armory VI
                # timePasses = True
            elif commandWords[0].lower() == "me":
                player.showSummary()

            elif commandWords[0].lower() == "save":
                print("Saving game...")
                time.sleep(1)
                print("Game saved.")
                time.sleep(1)
                saveGame()

            elif commandWords[0].lower() == "pickup":  #can handle multi-word objects
                targetName = command[7:]
                target = player.location.getItemByName(targetName)
                if target != False:
                    player.pickup(target)
                    print()
                    commandSuccess = False
                else:
                    print("No such item.")
                    commandSuccess = False

            elif commandWords[0].lower() == "inventory":
                player.showInventory()

            elif commandWords[0].lower() == "inspect":
                target = command[8:]
                flag = False
                for i in player.location.items:
                    if target.lower() == i.name.lower():
                        flag = True
                        print(i.desc)
                        print()
                        commandSuccess = False
                        break
                if not flag:
                    print("That item is not in this room! If you want to inspect an item in your inventory, use the command while in your inventory!")
                    print()
                    commandSuccess = False
                


            elif commandWords[0].lower() == "talk":
                targetName = command[5:]
                target = player.location.getNPCByName(targetName)
                if target != False:
                    target.dialogue(player)
                else:
                    print("There's nobody with that name here!")
                    commandSuccess = False

            elif commandWords[0].lower() == "help":
                showHelp()

            elif commandWords[0].lower() == "map":
                showMapCurrentRoom(player)

            elif commandWords[0].lower() == "exit":
                playing = False

            elif commandWords[0].lower() == "attack":
                if player.location.monsters == []:
                    print("You're safe. No enemies to attack in this room.")
                    commandSuccess = False
                else:
                    if player.location.level == 7: #Final boss dialogue
                        clear()
                        finalboss_dialogue(player)
                    combatSequence(player.location.monsters,player)

            elif commandWords[0].lower() in ['equip','use']:
                print("You need to be in your inventory to use that command!")
                print()
                commandSuccess = False

            else:
                print()
                print("Ye can't do that! Tis not a valid command!")
                print()
                commandSuccess = False

    if timePasses == True:
        updater.updateAll()



