import socket
import request
import _thread
from routes import (
    error,
    url_dict,
)
import routes.route_index
import routes.route_todo
import routes.api_route
import routes.route_chatroom


def obtain_data(connection, ip):
    rs = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        rs += r
        if len(r) < buffer_size:
            break
    if len(r) <= 0:
        print('浏览器又蛋疼了')
    else:
        response = response_for_path(rs, ip, connection)
        connection.sendall(response)
    connection.close()


def response_for_path(r, ip, connection):
    requests = request.Request(r)
    requests.ip = ip
    requests.connection = connection
    path = requests.get('path')
    route = url_dict.get(path, error)
    return route(requests)


def run(host, port):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()
        while True:
            connection, ip = s.accept()
            _thread.start_new_thread(obtain_data, (connection, ip))


if __name__ == '__main__':
    config = {
        'host': '0.0.0.0',
        'port': 233,
    }
    run(**config)
