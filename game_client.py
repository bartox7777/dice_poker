import socket

PORT = 65432
FORMAT = "utf-8"
SERVER = "192.168.8.127"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(data):
    data = data.encode(FORMAT)
    client.send(data)  # 2048 bytes max

players_number = None
while not players_number:
    data = client.recv(2048)
    if data:
        print(data.decode(FORMAT))
        break

client.send(DISCONNECT_MESSAGE.encode(FORMAT))
client.close()