import socket
import sys
import time
from _thread import *
import threading
from hash import calcular_hash
def leer_archivo(file_name,sock):
    file = open(file_name, "w")
    # Leemos de a 1024 bytes
    archivo = sock.recv(1024).decode("utf-8")
    try:
        while archivo:
            file.write(archivo)
            archivo = sock.recv(1024).decode("utf-8")
    except TimeoutError:
        a = 1
    file.close()
    return
def leer_hash(sock,file_name):
    try:
        archivo = sock.recv(1024).decode("utf-8")
        while (archivo):
            archivo = sock.recv(1024).decode("utf-8")
    except TimeoutError:

        a = 1
    hash = calcular_hash(file_name)
    print(hash)
    print(archivo)
    return hash == archivo


def main(num_cliente, cantidad_conexiones):
    # Creamos el Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    # Parametros de la conexión
    server_address = ('localhost', 10000)
    # Generamos la conexión
    sock.connect(server_address)
    try:
        file_name = "ArchivosRecibidos/Cliente" + str(num_cliente) + "-Prueba-"+str(cantidad_conexiones)+".txt"
        # Lectura del archivo
        print("LEYENDO")
        leer_archivo(file_name,sock)
        print("LEIDO")
        sock.send("R".encode("utf-8"))
        r = leer_hash(sock, file_name)
        if r:
            sock.send(("E-" + str(num_cliente)).encode("utf-8"))
        else:
            sock.send(("F-" + str(num_cliente)).encode("utf-8"))
        print("Archivo recibido")
        
        # Abrimos el archivo para validar su consistencia
        print(calcular_hash(file_name))
    finally:
        print('Cerrando socket')
        sock.close()
clientes = 5
for i in range(clientes):
    t = threading.Thread(target=main, args=((i+1),clientes))
    t.start()