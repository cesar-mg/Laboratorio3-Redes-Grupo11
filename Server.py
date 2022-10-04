import socket
import time
import datetime    
from a import calcular_hash
import threading
import queue
lock = threading.Lock()
date = datetime.datetime.now()
name = str(date.year) + "-" + str(date.month) + "-" + str(date.day) + "-" + str(date.hour) + "-" + str(date.minute) + "-" + str(date.second)
            
num_conexiones = int(input("Ingrese el numero de clientes a esperar"))
f = int(input("Ingrese archivo que desea envíar. 1) Para 100mb 2) Para 250 mb."))
clientes_actuales = 0
tam = 0
if f == 1:
    path = "test_100.txt"
    tam = "100 mb"
else:
    path = "test_250.txt"
    tam = "250 mb"

def handle_client(connection, client_address):
        try:
            print('Conexion recibida de:', client_address)
            data = open(path,"r",encoding='utf-8')
            
            file = data.read()
            data.close()
            init = time.time()
            print("ENVIANDO")
            connection.send(file.encode("utf-8"))
            print("LISTO")
            fin = time.time()
            connection.recv(1024)
            
            tiempo = fin - init
            
            connection.send(calcular_hash(path).encode())
            ok = connection.recv(1024).decode("utf-8").split("-")
            lock.acquire()
            log = open("Logs/"+name+"-log.txt","w")
            log.write("Nombre del archivo: " + path + " Tamanio del archivo: " + tam)
            log.write("Cliente: " + ok[1] )
            if ok[0] == "E":
                log.write(" Entrega Exitosa")
            else:
                log.write(" Entrega Fallida")
            log.write("El tiempo calculado fue de: " + str(tiempo) +"\n")
            print('Archivo enviado')
            log.close()
            lock.release()
        finally:
            connection.close()
            
def main():
    global clientes_actuales
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print('Iniciando {} en el puerto {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(num_conexiones)

    while True:
        # Wait for a connection
        print('Esperando conexiones')
        connection, client_address = sock.accept()
        clientes_actuales +=1
        t = threading.Thread(target=handle_client, args=(connection, client_address))
        t.start()
main()
