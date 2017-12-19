from routes import (
    response_with_headers,
    obtain_user,
    redirect,
    validate_login,
    template,
    route,
)
from websocket import (
    WebSocket,
    clients,
)


@route('/api/chatroom')
@validate_login
def api_chatroom(requests):
    b = WebSocket.hand_shaken(requests)
    username = obtain_user(requests).username
    WebSocket.send('加入了聊天室', username)
    if b is False:
        return bytes(response_with_headers(404), encoding='utf-8')
    else:
        while True:
            r = requests.connection.recv(1024)
            if WebSocket.decode(r) == 'quit':
                clients.pop(obtain_user(requests).username)
                WebSocket.send('退出了聊天室', username)
                break
            else:
                WebSocket.send(r, username)
        return redirect('/')


@route('/chatroom')
@validate_login
def chatroom(_):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    body = template('chatroom')
    data = header + body
    return data.encode(encoding='utf-8')
