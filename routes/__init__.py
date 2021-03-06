import request
from models.user import User
import json
import redis
import uuid
from functools import wraps
from gzip import compress
from hashlib import md5


r = redis.StrictRedis(charset="utf-8", decode_responses=True)
url_dict = {}


def route(path):
    def func(f):
        url_dict[path] = f
        return f
    return func


def error(_):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(404, headers)
    body = '\r\n<h1>NOT FOUND</h1>'
    data = header + '\r\n' + body
    return data.encode(encoding='utf-8')


def response_with_headers(code, headers=None):
    codes = {
        101: 'HTTP/1.1 101 Switching Protocols\r\n',
        200: 'HTTP/1.1 200 OK\r\n',
        404: 'HTTP/1.1 404 NOT FOUND\r\n',
        302: 'HTTP/1.1 302\r\n',
        304: 'HTTP/1.1 304\r\n',
    }
    header = codes[code]
    if headers is not None:
        header += ''.join([
            '{}: {}\r\n'.format(k, v) for k, v in headers.items()
        ])
    return header + '\r\n'


def validate_login(f):
    @wraps(f)
    def vailedate(requests):
        u = obtain_user(requests)
        if u is not None:
            return f(requests)
        else:
            return redirect('/login')
    return vailedate


def validate_login_redirect(f):
    @wraps(f)
    def vailedate(requests):
        u = obtain_user(requests)
        if u is not None:
            return redirect('/')
        else:
            return f(requests)
    return vailedate


def validate_token(f):
    def validate(requests):
        u = obtain_user(requests)
        if u is not None:
            token = requests.get('body').get('token')
            if r.exists(token) and r.get(token) == u.id:
                r.delete(token)
                return f(requests)
            else:
                return bytes(response_with_headers(404), encoding='utf-8')
        else:
            return redirect('/login')
    return validate


def new_token(requests):
    token = str(uuid.uuid4())
    r.set(token, obtain_user(requests).id, 18000)
    return token


def obtain_user(requests):
    cookies = requests.get('cookies')
    cookie = cookies.get('session_id', None)
    u = get_cookie_id(cookie)
    if u is not None:
        return User.find(id=u)[0]
    return None


def redirect(url, header=None):
    headers = {
        'Location': url,
    }
    if header is not None:
        headers.update(header)
    h = response_with_headers(302, headers) + '\r\n'
    return h.encode()


def template(name, **kwargs):
    path = 'htmls/{}.html'.format(name)
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    if len(kwargs) > 0:
        for k, v in kwargs.items():
            name = '{{' + str(k) + '}}'
            data = data.replace(name, kwargs[k])
    return data


@route('/cover')
def cover(requests):
    cover_name = requests.query.get('img', None)
    if cover_name is None:
        return error(requests)
    else:
        postfix = cover_name.split('.', 1)[1]
        path = 'covers/' + cover_name
        headers = {
            'Content-Type': 'image/{}'.format(postfix),
        }
        if 'gzip' in requests.headers['Accept-Encoding']:
            headers['Content-Encoding'] = 'gzip'
        with open(path, 'rb') as f:
            read_file = f.read()
            hash_value = md5(read_file).hexdigest()
            if 'If-None-Match' in requests.headers and hash_value == requests.headers['If-None-Match']:
                header = response_with_headers(304, headers)
                data = bytes(header, encoding="utf-8")
            else:
                headers['ETag'] = hash_value
                header = response_with_headers(200, headers)
                data = bytes(header, encoding="utf-8") + compress(read_file) if 'Content-Encoding' in headers else read_file
            return data


@route('/static')
def static(requests):
    file_name = requests.query.get('file', None)
    if file_name is None:
        return error(requests)
    else:
        postfix = file_name.split('.', 1)[1]
        path = 'static/' + file_name
        if postfix == 'css':
            type_ = 'text/css'
        else:
            type_ = 'application/x-javascript'
        headers = {
            'Content-Type': type_
        }
        with open(path, 'rb') as f:
            header = response_with_headers(200, headers)
            data = bytes(header, encoding="utf-8") + f.read()
            return data


def json_response(data):
    headers = {
        'Content-Type': 'application/json'
    }
    header = response_with_headers(200, headers)
    body = json.dumps(data, ensure_ascii=False)
    data = header + body
    return data.encode(encoding='utf-8')


def set_cookie(cookie, user_id):
    r.set(cookie, user_id, 18000)


def get_cookie_id(cookie):
    if r.exists(cookie):
        return r.get(cookie)
    else:
        return None

