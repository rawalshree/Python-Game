from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# create Black Magic:
fire = Spell("Fire", 30, 150, "Black")
thunder = Spell("Thunder", 40, 200, "Black")
blizzard = Spell("Blizzard", 35, 170, "Black")
meteor = Spell("Meteor", 20, 110, "Black")
quake = Spell("Quake", 25, 130, "Black")

# create White Magic:
cure = Spell("Cure", 40, 1000, "White")
cura = Spell("Cura", 60, 1500, "White")
#curaga = Spell("Curaga", 90, 4000, "White")

# Create some Items
potion = Item("Potion", "Potion", "Heals 50 Hp", 50, 10)
hipotion = Item("Hipotion", "Potion", "Heals 100 Hp", 100, 5)
superpotion = Item("Superpotion", "Potion", "Heals 500 Hp", 500, 5)
elixir = Item("Elixir", "Elixir", "Fully restores HP/MP of one party member", 9999, 5)
superelixir = Item("Superelixir", "Elixir", "Fully restores Party's HP/MP", 9999, 2)
grenade = Item("Grenade", "Attack", "Deals 500 damage", 500, 3)


player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_magic = [fire, thunder, blizzard, cure]

player_items = [{"item": potion, "quantity": 10},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixir, "quantity": 5},
                {"item": superelixir, "quantity": 2},
                {"item": grenade, "quantity": 5}]
enemy_items = [{"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Shree", 3000, 300, 200, 34, player_magic, player_items)
player2 = Person("Rawal", 2500, 200, 150, 34, player_magic, player_items)
player3 = Person("Flash", 1200, 150, 100, 34, player_magic, player_items)

enemy2 = Person("De-voe", 1400, 200, 700, 300, enemy_magic, enemy_items)
enemy1 = Person("Savtar", 9000, 500, 550, 30, enemy_magic, enemy_items)
enemy3 = Person("Thorne", 1400, 200, 700, 300, enemy_magic, enemy_items)

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "ENEMY ATTACKS" + bcolors.ENDC)

while running:
    print("========================")
    print("\nNAME                 HP                                   MP")
    for player in players:
        player.get_stats()

    print(bcolors.BOLD + bcolors.FAIL + "\n\nENEMY NAME          ENEMY HP                                        "
          + "ENEMY MP" + bcolors.ENDC)
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        if player.get_hp() != 0:
            player.choose_action()
            choice = input("    Choose action: ")
            index = int(choice) - 1

            if index == 0:
                dmg = player.generate_damage()
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(dmg)
                print("\n" + bcolors.OKBLUE + player.name + " attacked", enemies[enemy].name, "for", dmg, "points of damage" + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has Died.")
                    del enemies[enemy]

            elif index == 1:
                player.choose_magic()
                magic_choice = int(input("    Choose Magic: ")) - 1
                spell = player.magic[magic_choice]
                magic_dmg = spell.generate_damage()

                if magic_choice == -1:
                    continue

                current_mp = player.get_mp()

                if spell.cost > current_mp:
                    print(bcolors.FAIL, "\nNot Enough MP\n", bcolors.ENDC)
                    continue

                player.reduce_mp(spell.cost)

                if spell.type == 'White':
                    player.heal(magic_dmg)
                    print(bcolors.OKBLUE, "\n", spell.name, "heals for", str(magic_dmg), " Hp.", bcolors.ENDC)
                elif spell.type == 'Black':
                    enemy = player.choose_target(enemies)
                    if enemies[enemy].get_hp() != 0:
                        enemies[enemy].take_damage(magic_dmg)
                        print(bcolors.OKBLUE, "\n" + spell.name, "deals ", str(magic_dmg), " points of damage to " + enemies[enemy].name + bcolors.ENDC)
                    else:
                        print("\n" + bcolors.OKBLUE + enemies[enemy].name + " is already dead" + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has Died.")
                    del enemies[enemy]

            elif index == 2:
                player.choose_items()
                item_choice = int(input("    Choose item: ")) - 1
                if item_choice == -1:
                    continue

                item = player.items[item_choice]["item"]

                if player.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL + "\n", "None left........" + bcolors.ENDC)
                    continue
                else:
                    player.items[item_choice]["quantity"] -= 1

                if item.type == "Potion":
                    player.heal(item.prop)
                    print(bcolors.OKBLUE, "\n", item.name, "heals for", item.prop, " Hp.", bcolors.ENDC)
                elif item.type == "Elixir":
                    if item.name == "Superelixir":
                        for i in players:
                            player.hp = player.maxhp
                            player.mp = player.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                    print(bcolors.OKGREEN, "\n", item.name, "Fully restores HP/MP", bcolors.ENDC)
                elif item.type == "Attack":
                    enemy = player.choose_target(enemies)
                    if enemies[enemy].get_hp() != 0:
                        enemies[enemy].take_damage(item.prop)
                        print(bcolors.FAIL, "\n", item.name, "deals ", item.prop, " points of damage to " + enemies[enemy].name + bcolors.ENDC)
                    else:
                        print("\n" + bcolors.OKBLUE + enemies[enemy].name + " is already dead" + bcolors.ENDC)

                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name + " has Died.")

    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if Player Won
    if defeated_enemies == len(enemies):
        print(bcolors.OKGREEN + " You WIN!!!" + bcolors.ENDC)
        running = False
        continue

    # Check if Enemy Won
    if defeated_players == len(players):
        print(bcolors.FAIL + " You LOSE!!!" + bcolors.ENDC)
        running = False
        continue

    # Enemy attack phase
    for enemy in enemies:
        if enemy.get_hp() != 0:
            enemy_choice = random.randrange(0, 2)

            if enemy_choice == 0:
                target = random.randrange(0, len(players))
                enemy_dmg = enemy.generate_damage()
                if players[target].get_hp() != 0:
                    players[target].take_damage(enemy_dmg)
                    print("\n" + bcolors.FAIL + enemy.name + " attacks", players[target].name, "for ", enemy_dmg, bcolors.ENDC)
                    if players[target].get_hp() == 0:
                        print("\n" + bcolors.FAIL + players[target].name + " is dead" + bcolors.ENDC)

            elif enemy_choice == 1:
                spell, magic_dmg = enemy.choose_enemy_spell()
                enemy.reduce_mp(spell.cost)

                if spell.type == 'White':
                    enemy.heal(magic_dmg)
                    print(bcolors.FAIL, "\n", spell.name, "heals ", enemy.name, "for", str(magic_dmg), " Hp.", bcolors.ENDC)
                elif spell.type == 'Black':
                    target = random.randrange(0, 3)

                    if players[target].get_hp() != 0:
                        players[target].take_damage(magic_dmg)
                        print(bcolors.FAIL, "\n" + enemy.name + "'s " + spell.name, "deals ", str(magic_dmg), " points of damage to " + players[target].name + bcolors.ENDC)
                        if players[target].get_hp() == 0:
                            print("\n" + bcolors.FAIL + players[target].name + " is dead" + bcolors.ENDC)
