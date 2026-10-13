import socket
from _thread import *
import sys
from network import Network
from Components.bullet import Bullet, Bullets
from Components.format_data import convert_initial_message, build_server_reply, unpack_server_reply, unpack_client_reply, build_client_reply
from Components.settings import *

server = socket.gethostbyname("0.0.0.0") # listens to everything
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print ("Test client sending packets to IP {0}, via port {1}\n".format(server, port))

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)    # how many things it is going to allow to connect
print("Server started, waiting for connection")

spaceship_positions = [(0, HEIGHT//2, SPACESHIP_SIZE[0], SPACESHIP_SIZE[1]), (WIDTH - SPACESHIP_SIZE[0], HEIGHT//2, SPACESHIP_SIZE[0], SPACESHIP_SIZE[1])]
bullets = [Bullets(1), Bullets(-1)]
ammo = [0.0, 0.0]
sb_charge = [0, 0]
health = [10, 10]

class Killer:
    def __init__(self):
        self.do_kill = False
    def kill(self):
        print("killing")
        self.do_kill = True
        # connect to the socket then close it
        _ = Network()

def threaded_client(conn, current_player, killer):
    initial_message = list(spaceship_positions[current_player])
    initial_message.append(current_player)
    initial_message += list(spaceship_positions[int(not current_player)])
    conn.send(str.encode(convert_initial_message(initial_message)))
    reply = ""
    while True:
        try:
            data = conn.recv(2048) # receives the data
            data = data.decode("utf-8") # decode data, arg is the number of bits to receive
            if data == "Kill":
                conn.sendall(str.encode(""))
                break
            
            ship_position, bullet_created = unpack_client_reply(data)
            spaceship_positions[current_player] = ship_position
            
            if bullet_created != ():
                bullets[current_player].add_bullet(bullet_created)
            
            bullets[current_player].move()
            
            if not ship_position:
                print("disconnected")
                break
            
            else:
                reply = build_server_reply(current_player, spaceship_positions, bullets, ammo, sb_charge)
                #print(5, reply) # bullets is class

                print("Received:", data)
                print("sending:", reply)
                
            conn.sendall(str.encode(reply)) # encodes with utf-8        
        except:
            pass#print("error")
    
    print("lost connection")
    conn.close()
    killer.kill()
    
killer = Killer()
current_player = 0
while True:
    conn, addr = s.accept() # accepts incoming connections, address = ip address
    print("Connected to:", addr)
    
    if killer.do_kill == True:
        raise TimeoutError("Client disconnected")
    
    start_new_thread(threaded_client, (conn, current_player, killer)) # allows the program to continue to look for new connections while client program runs
    current_player += 1