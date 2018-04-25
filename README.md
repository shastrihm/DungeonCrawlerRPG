# You Are Only A Pawn
A text based, chess themed dungeon crawler RPG 

Brief description:

    This is a dungeon crawler RPG where the player is thrown into a 'chessboard' (really a castle) like map 
    (where each room is a 'square') and has to feel their way to the end. 
    They will encounter strong and weak monsters, friendlies, and various items that will both help and harm their journey. 
    As you progress deeper into the castle, you will level up and get stronger by gaining experience. You will also be able
    to obtain stronger items-- but the monsters get stronger as well. While no easy task, you will be victorious if you defeat the 
    King and Queen in their bedroom and outwit the GateKeeper in the throneroom. 

Gameplay explanation:

    Map:
        This game is a dungeon crawler, so you will be traversing rooms in a map. The map is randomly generated-- 8 levels, and the 
        first 6 levels have 8 rooms each, with the final two rooms being boss battles. The connections between rooms and levels are 
        randomly generated, as well as the number of and type of monsters. You cannot go to other rooms without defeating all monsters 
        in your current room or using an escape rope (see item section). In general the monsters get stronger as you progress. To
        progress to the next level, the player will need to obtain a Key (1 key per level), which is also randomly hidden in a room
        in the level. 
    Combat: 
        The combat is turn based, between all the monsters in the player's current location and the player themself. 
        The monsters attack the player all at once while the player must choose a single monster to focus on each turn. 
        The player can also use items during the battle, like drinking a health potion to restore health or throwing an 
        escape rope to flee from the battle. The damage calculation is done through a special damage formula based on the
        monster's and player's attack/defense/accuracy stats. Monsters drop various items (according to their droptable, 
        which varies by monster type) that can be looted by the player.
    Items: 
        There are four classes of items: keys, health potions, escape ropes, and equipment.
            Keys: keys are as described earlier in the map section. They unlock doors to the next level.
            Health Potions: There are three types of health potions: minor(heal 30% health), greater(heal 50% health), 
            and maximum(heal 100% health). They have different probabilities of dropping, based on the monster dropping them. 
            They can be consumed in battle or in world through the inventory 'use' command. 
            Escape Ropes: Escape ropes are meant to be a lifeline for when you have low health and need to get away from enemies. 
            They can be used in battle to escape from combat or they can be used in a room if you want to escape that room without confronting the monsters. In each case, they transport you to a random neighboring room (which may or may not have monsters)
            Equipment: There are 8 different weapons and 8 different armors. They have different attack/defense bonuses, 
            depending on which monster they drop from (stronger monsters drop stronger equipment). 
            You can equip them using the 'equip' command in the inventory.
    NPCs:
        Paul the Polite Priest is a Medic that can heal you to full health. He is found in the VIII room of each level
        (excluding the two boss rooms). The Gatekeeper is also an NPC the player encounters at the very end of the game. 
    Boss battle:
        In the second to last room, the player must defeat the King+Queen in the Queen's Bedroom. This boss battle 
        is not easy, as it is between two very powerful monsters (w/ 40/60 60/40 att/def respecively) that heal each 
        other by random amounts each turn. If you defeat them, you have to outwit the Gatekeeper to get the proper win 
        screen (although you can consider the game completed regardless at that point)

Since this game takes a decent chunk of time to complete, there is an option to create a save file in the game's directory. This allows you to quit the game and come back to it at a later time. 
