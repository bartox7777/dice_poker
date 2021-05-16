# help: TechWithTim
import socket
import threading
import json

PLAYERS = input("Number of players: ")

PORT = 65432
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
LENGTH = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

player_dict = {
    "players": PLAYERS,
    "player_id": None,
    "turn": 1,
    "start": False,
    "players_points": None,
    "blocked_points": None,
    "dice": None,
    "blocked_dice": None
}

player_socket = {}
player_data_to_send = {}

def prep_data(data):
    data = json.dumps(data).encode(FORMAT)
    data += b" " * (LENGTH - len(data))
    return data

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    player_id = str(threading.activeCount() - 1)
    player_socket[player_id] = conn

    player_dict_temp = player_dict.copy()
    player_dict_temp["player_id"] = player_id

    player_data_to_send[player_id] = player_dict_temp

    conn.send(prep_data(player_dict_temp))

    connected = True

    while connected:
        try:
            data = json.loads(conn.recv(LENGTH).decode(FORMAT))
        except:
            continue
        if data:
            print(f"[RECEIVED DATA] from {addr}: {data}")
            if data == DISCONNECT_MESSAGE:
                connected = False
                break
            if data.get("dice"):
                for player_id, socket in player_socket.items():
                    player_data_to_send[player_id]["dice"] = data["dice"]
                    player_data_to_send[player_id]["blocked_dice"] = data["blocked_dice"]
                    socket.send(prep_data(player_data_to_send[player_id]))
            if data.get("dice") is None: # end of turn
                for player_id, socket in player_socket.items():
                    player_data_to_send[player_id]["dice"] = None
                    turn = data["turn"] + 1
                    if turn > int(PLAYERS):
                        turn = 1
                    player_data_to_send[player_id]["turn"] = turn
                    player_data_to_send[player_id]["players_points"] = data["players_points"]
                    player_data_to_send[player_id]["blocked_points"] = data["blocked_points"]
                    player_data_to_send[player_id]["blocked_dice"] = [False] * 5
                    socket.send(prep_data(player_data_to_send[player_id]))
    print(f"[CLOSE CONNECTION] connection closed {addr}")
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

        if (threading.activeCount() - 1) == int(PLAYERS):  # all players connected
            player_dict["start"] = True
            for player_id, player in player_socket.items():
                player_data_to_send[player_id]["start"] = True
                player.send(prep_data(player_data_to_send[player_id]))


print("[STARTING] starting server...")
start()