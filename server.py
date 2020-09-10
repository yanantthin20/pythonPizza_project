import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), 1239))

serversocket.listen(5)
print ('server started and listening')
while 1:
    (clientsocket, address) = serversocket.accept()
    print ("connection found!")
    data = clientsocket.recv(2048).decode()
    print(data)
    r='Receieve'
    clientsocket.send(r.encode())

clientsocket.close()