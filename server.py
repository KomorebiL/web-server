import socket
from route import *


def obtain_data(connection):
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        if len(r) < buffer_size:
            break
    return request


def run(host, port):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()
        while True:
            connection, ip = s.accept()
            r = obtain_data(connection)
            if len(r) <= 0:
                print('浏览器又蛋疼了')
            else:
                response = response_for_path(r.decode('utf-8'))
                connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    run('0.0.0.0', 233)