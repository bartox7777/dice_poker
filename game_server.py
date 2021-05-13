# help: TechWithTim
# TODO: replace it to game.py
import socket
import threading
import json

PLAYERS = input("Number of players: ")

PORT = 65432
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

player_dict = {
    "players": PLAYERS,
    "player_id": None,
    "turn": None,
    "start": False,
    "players_points": None,
    "blocked_points": None
}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    player_dict_temp = player_dict.copy()
    player_dict_temp["player_id"] = str(threading.activeCount() - 1)
    json_dict = json.dumps(player_dict_temp)
    conn.send(json_dict.encode(FORMAT))

    connected = True

    while connected:
        data = conn.recv(2048).decode(FORMAT)
        if data:
            if data == DISCONNECT_MESSAGE:
                connected = False
            print(f"[RECEIVED DATA] from {addr}: {data}")
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

        if (threading.activeCount() - 1) == PLAYERS:  # all players connected
            pass


print("[STARTING] starting server...")
start()
