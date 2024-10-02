import socketserver
import threading

class ChatRoom:
    def __init__(self, room_id, room_name='Food'):
        self.room_id = room_id
        self.room_name = room_name
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        self.clients.remove(client)

    def broadcast(self, message):
        for client in self.clients:
            client.sendall(f"{message}\n".encode())



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
  allow_reuse_address = True


class ChatHandler(socketserver.BaseRequestHandler):
    rooms = {}

    def handle(self):
        self.room = None
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            data = data.decode().strip()
            if data.startswith('`join'):
                _, room_id, chatter_name = data.split()
                self.join_room(room_id, chatter_name)
            elif data.startswith('`exit'):
                self.request.close()
                break
            else:
                self.send_message(data)

    def join_room(self, room_id, chatter_name):
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id)
        self.room = self.rooms[room_id]
        self.room.add_client(self.request)
        self.room.broadcast(f"A new client {chatter_name} has joined chat_room {room_id}.")

    def send_message(self, message):
        if self.room:
            self.room.broadcast(message)
        else:
            self.request.sendall(b"Join a room first!\n")

if __name__ == "__main__":
    with ThreadedTCPServer(("localhost", 9999), ChatHandler) as server:
        server.serve_forever()            