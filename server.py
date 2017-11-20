import socket
import request
import _thread
from routes import error
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
        response = response_for_path(rs, ip)
        connection.sendall(response)
    connection.close()


def response_for_path(r, ip):
    requests = request.Request(r)
    requests.ip = str(ip[0])
    path = requests.get('path')
    rs = {}
    us = [
        routes.route_index.route_dict(),
        routes.api_route.route_dict(),
        routes.route_todo.route_dict(),
        routes.route_chatroom.route_dict(),
    ]
    for u in us:
        rs.update(u)
    route = rs.get(path, error)
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