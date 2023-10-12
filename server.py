import socket
from _thread import *
import sys
from network import Network
from Components.bullet import Bullet, Bullets
from Components.format_data import convert_initial_message, build_server_reply, unpack_server_reply, unpack_client_reply, build_client_reply
from Components.settings import *

server = "10.100.227.43" # local address!!!!!
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.bind((server, port))
except socket.error as e:
  print(e)

s.listen(2)  # how many things it is going to allow to connect
print("Server started, waiting for connection")

spaceship_positions = [(0, HEIGHT//2, SPACESHIP_SIZE[0], SPACESHIP_SIZE[1]), (WIDTH - SPACESHIP_SIZE[0], HEIGHT//2, SPACESHIP_SIZE[0], SPACESHIP_SIZE[1])]
bullets = [Bullets(), Bullets()]
ammo = [0.0, 0.0]
sb_charge = [0, 0]
health = [10, 10]

class Killer:
  def __init__(self):
    self.do_kill = False
  def kill(self):
    self.do_kill = True
    # connect to the socket then close it
    _ = Network()

def threaded_client(conn, current_player, killer):
  initial_message = list(spaceship_positions[current_player])
  initial_message.append(current_player)
  conn.send(str.encode(convert_initial_message(initial_message)))
  reply = ""
  while True:
    try:
      data = conn.recv(2048) # receives the data
      data = data.decode("utf-8") # decode data, arg is the number of bits to receive
      # = unpack_client_reply(data)
      
      if not data:
        print("disconnected")
        break
      
      else:
        reply = build_server_reply(current_player, spaceship_positions, bullets, ammo, sb_charge)

        print("Received:", data)
        print("sending:", reply)
      
      conn.sendall(str.encode(reply)) # encodes with utf-8
    
    except:
      print("error")
  
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