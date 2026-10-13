import socket

school_server = "10.100.224.182"
surface_server = "192.168.0.21"
laptop_server = "192.168.0.79"

class Network:
  def __init__(self):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server = "10.100.224.98" # SERVER address!!!!!
    self.port = 5555
    self.addr = (self.server, self.port)
    print(1)
    self.init_pos = self.connect()
    print(2)
  
  def get_init_pos(self):
    return self.init_pos
    
  def connect(self):
    try:
      self.client.connect(self.addr)
      return self.client.recv(2048).decode("utf-8")
    except:
      pass
  
  def send(self, data):
    try:
      self.client.send(str.encode(data))
      return self.client.recv(2048).decode("utf-8") 
    except socket.error as e:
      print(e)
