import hashlib
from base64 import b64encode, b64decode
import struct
from routes import (
    response_with_headers,
    obtain_user,
)


class WebSocket:

    @classmethod
    def hand_shaken(cls, requests):
        GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        try:
            key = requests.headers.get('Sec-WebSocket-Key')
            token = b64encode(hashlib.sha1(str.encode(key + GUID)).digest())
            headers = {
                'Upgrade': 'websocket',
                'Connection': 'Upgrade',
                'Sec-WebSocket-Accept': token.decode('utf-8'),
                'WebSocket-Location': 'ws://127.0.0.1:233/api/chatroom',
                'WebSocket-Origin': requests.headers.get('Origin'),
            }
            data = response_with_headers(101, headers)
            requests.connection.sendall(data.encode(encoding='utf-8'))
            username = obtain_user(requests).username
            clients[username] = requests.connection
            return True
        except:
            print('握手失败')
            return False

    @staticmethod
    def encode(data):
        head = b'\x81'
        if len(data) < 126:
            head += struct.pack('B', len(data))
        elif len(data) <= 0xFFFF:
            head += struct.pack('!BH', 126, len(data))
        else:
            head += struct.pack('!BQ', 127, len(data))
        return head + data

    @staticmethod
    def decode(data):
        if not len(data):
            return False
        length = data[1] & 127
        if length == 126:
            mask = data[4: 8]
            raw = data[8:]
        elif length == 127:
            mask = data[10: 14]
            raw = data[14:]
        else:
            mask = data[2:6]
            raw = data[6:]
        ret = ''
        for cnt, d in enumerate(raw):
            ret += chr(d ^ mask[cnt % 4])
        return ret

    @classmethod
    def send(cls, data, username):
        if type(data) is bytes:
            data = cls.decode(data)
        data = '{}: {}'.format(username, data)
        data = bytes(data, encoding='utf-8')
        for c in clients.values():
            c.sendall(cls.encode(data))


clients = {}
