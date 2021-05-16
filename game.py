# coding: utf-8
# POKEROWE KOŚCI (inspiracja: https://www.kurnik.pl/kosci/)
import os
import sys
import json
import socket
import pygame
from random import randint
from objects import Die, Dice, Table

pygame.init()

DICE_X = 1200
DICE_Y_SPACE = 120
DICE_PADDING_TOP = 70
GREEN_BG = (48, 128, 72)
DARK_WHITE = (220, 220, 210)
DIE_6_PATH = os.path.join("data", "die_6.png")

PORT = 65432
FORMAT = "utf-8"
SERVER = input("Server IP: ")
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
LENGTH = 2048

def prep_data(data):
    data = json.dumps(data).encode(FORMAT)
    data += b" " * (LENGTH - len(data))
    return data

pygame.display.set_caption("Dice poker")
pygame.display.set_icon(pygame.image.load(DIE_6_PATH))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setblocking(False)
client.connect_ex(ADDR)

data = None
while not data:
    try:
        data = json.loads(client.recv(LENGTH).decode(FORMAT))
    except:
        continue
    if data:
        players = int(data["players"])
        player_move = int(data["turn"])
        player_id = int(data["player_id"])
        break

def get_random_dice(dice_group, number_of_dice=5):
    if len(dice_group) == 0:
        for i in range(number_of_dice):
            dice_group.add(Die(randint(1, 6), DICE_X, (i+1)*DICE_Y_SPACE+DICE_PADDING_TOP))
    else:
        new_dice_group = Dice()
        for die in dice_group:
            if die.blocked:
                new_dice_group.add(die)
            else:
                new_dice_group.add(Die(randint(1, 6), die.x, die.y))
        dice_group.empty()
        for die in new_dice_group:
            dice_group.add(die)

    dice_numbers = {
        "dice": [die.die_number for die in dice_group],
        "blocked_dice": [die.blocked for die in dice_group]
    }
    client.send(prep_data(dice_numbers))

screen = pygame.display.set_mode(size=(1900, 1000), flags=pygame.RESIZABLE)

dice_group = Dice()
table = Table(screen, DARK_WHITE, 500, 120, 420, 720, players)

shuffle_times = 0
auto_shuffle = True
all_connected = False
table.draw()

while True:
    try:
        data = json.loads(client.recv(LENGTH).decode(FORMAT))
        if data:
            print(f"[RECEIVED DATA] {data}")
            if data["start"]:
                # if data["blocked_dice"]:
                #     i = 0
                #     for die in dice_group:
                #         if data["blocked_dice"][i] and not die.blocked:
                #             die.change_state()
                #         i += 1

                all_connected = True
                player_move = data["turn"]
                if player_id == data["turn"] and auto_shuffle:
                    shuffle_times = 0
                    dice_group.empty()
                    get_random_dice(dice_group)
                    auto_shuffle = False
                if player_id != data["turn"]: # not turn of client
                    auto_shuffle = True
                    if data.get("dice"):
                        dice_group.empty()
                        i = 0
                        for die_number in data["dice"]:
                            dice_group.add(Die(die_number, DICE_X, (i+1)*DICE_Y_SPACE+DICE_PADDING_TOP, data["blocked_dice"][i]))
                            i += 1
                if data["players_points"]:
                    table.blocked_points = data["blocked_points"]
                    table.players_points = data["players_points"]
                    table.points_to_text()
    except:
        pass

    mouse_pos = pygame.mouse.get_pos()

    if table.blocked_points[players-1].count(True) == 17: # end of game
        player_total = {}
        totals = []
        won = []
        for i in range(players):
            player_total[i+1] = table.players_points[i][16]
            totals.append(table.players_points[i][16])
        totals = sorted(totals, reverse=True)
        player_total = sorted(player_total.items(), key=lambda x: x[1], reverse=True)
        for i in range(totals.count(totals[0])):
            won.append(player_total[i][0])
        if len(won) == players:
            print("Tie!")
        else:
            print("Won: ", end="")
            [print(player) for player in won]
        break  # TODO: info about won

    if data["turn"] == player_id and all_connected:
        if table.update(dice_group, player_move, mouse_pos): # clicked
            data["players_points"] = table.players_points
            data["blocked_points"] = table.blocked_points
            data["dice"] = None
            dice_group.empty()
            client.send(prep_data(data))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.send(prep_data(DISCONNECT_MESSAGE))
            client.close()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and player_move == player_id and all_connected:  # TODO: button to shuffle dice
            changed_state = False
            for die in dice_group:
                if die.rect.collidepoint(mouse_pos):
                    die.change_state()
                    changed_state = True
            if not changed_state and shuffle_times < 2:
                shuffle_times += 1
                get_random_dice(dice_group)

    screen.fill(GREEN_BG)
    dice_group.draw(screen)
    table.draw()
    pygame.display.flip()