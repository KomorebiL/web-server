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
        en_bytes = b''
        cn_bytes = []
        if len(data) < 6:
            return ''
        v = data[1] & 0x7f
        if v == 0x7e:
            p = 4
        elif v == 0x7f:
            p = 10
        else:
            p = 2
        mask = data[p:p + 4]
        data = data[p + 4:]
        for k, v in enumerate(data):
            nv = chr(v ^ mask[k % 4])
            nv_bytes = nv.encode()
            nv_len = len(nv_bytes)
            if nv_len == 1:
                en_bytes += nv_bytes
            else:
                en_bytes += b'%s'
                cn_bytes.append(ord(nv_bytes.decode()))
        if len(cn_bytes) > 2:
            cn_str = ''
            clen = len(cn_bytes)
            count = int(clen / 3)
            for x in range(0, count):
                i = x * 3
                b = bytes([cn_bytes[i], cn_bytes[i + 1], cn_bytes[i + 2]])
                cn_str += b.decode()
            new = en_bytes.replace(b'%s%s%s', b'%s')
            new = new.decode()
            res = (new % tuple(list(cn_str)))
        else:
            res = en_bytes.decode()
        return res

    @classmethod
    def send(cls, data, username):
        if type(data) is bytes:
            data = cls.decode(data)
        data = '{}: {}'.format(username, data)
        data = bytes(data, encoding='utf-8')
        for c in clients.values():
            c.sendall(cls.encode(data))


clients = {}
