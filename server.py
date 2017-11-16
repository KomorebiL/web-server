import socket
import request
from routes import error
import routes.route_index
import routes.api_route


def obtain_data(connection):
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        if len(r) < buffer_size:
            break
    return request


def response_for_path(r, ip):
    requests = request.request(r)
    requests.ip = str(ip[0])
    path = requests.get('path')
    rs = {}
    us = [
        routes.route_index.route_dict(),
        routes.api_route.route_dict(),
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
            r = obtain_data(connection)
            if len(r) <= 0:
                print('浏览器又蛋疼了')
            else:
                response = response_for_path(r.decode('utf-8'), ip)
                connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    config = {
        'host': '0.0.0.0',
        'port': 233,
    }
    run(**config)