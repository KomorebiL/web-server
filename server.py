import socket


host = '0.0.0.0'
port = 233
s = socket.socket()
s.bind((host, port))
while True:
    s.listen(5)
    connection, ip = s.accept()
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        if len(r) < buffer_size:
            break
    print('ip:{}\nrequest:{}'.format(ip, request.decode('utf-8')))
    response = b'HTTP/1.1 200 OK\r\n\r\n<h1>Hello World!</h1>'
    connection.sendall(response)
    connection.close()
