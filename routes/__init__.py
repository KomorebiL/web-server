import request
from models.user import User
import json
import redis
import uuid


r = redis.StrictRedis(charset="utf-8", decode_responses=True)


def error(requests):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(404, headers)
    body = '\r\n<h1>NOT FOUND</h1>'
    data = header + '\r\n' + body
    return data.encode(encoding='utf-8')


def response_with_headers(code, headers=None):
    codes = {
        200: 'HTTP/1.1 200 OK\r\n',
        404: 'HTTP/1.1 404 NOT FOUND\r\n',
        302: 'HTTP/1.1 302\r\n'
    }
    header = codes[code]
    if headers is not None:
        header += ''.join([
            '{}: {}\r\n'.format(k, v) for k, v in headers.items()
        ])
    return header + '\r\n'


def validate_login(f):
    def vailedate(requests):
        u = obtain_user(requests)
        if len(u) > 0:
            return f(requests)
        else:
            return redirect('/login')
    return vailedate


def validate_login_redirect(f):
    def vailedate(requests):
        u = obtain_user(requests)
        if len(u) > 0:
            return redirect('/')
        else:
            return f(requests)
    return vailedate


def validate_token(f):
    def validate(requests):
        u = obtain_user(requests)
        if len(u) > 0:
            token = requests.get('body').get('token')
            if r.exists(token) and r.get(token) == u[0].id:
                r.delete(token)
                return f(requests)
            else:
                return bytes(response_with_headers(404), encoding='utf-8')
        else:
            return redirect('/login')
    return validate


def new_token(requests):
    token = str(uuid.uuid4())
    r.set(token, obtain_user(requests)[0].id, 18000)
    return token


def obtain_user(requests):
    cookies = requests.get('cookies')
    cookie = cookies.get('session_id', None)
    form = {
        'cookie': cookie,
    }
    u = User.find(**form)
    return u


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


def cover(requests):
    cover_name = requests.query.get('img', None)
    if cover_name is None:
        return error(requests)
    else:
        postfix = cover_name.split('.', 1)[1]
        path = 'covers/' + cover_name
        headers = {
            'Content-Type': 'image/{}'.format(postfix)
        }
        with open(path, 'rb') as f:
            header = response_with_headers(200, headers)
            data = bytes(header, encoding="utf-8") + f.read()
            return data


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
