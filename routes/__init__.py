import request
from models.user import User
import json


def error(requests):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(404, headers)
    body = '\r\n<h1>NOT FOUND</h1>'
    data = header + '\r\n' + body
    return data.encode(encoding='utf-8')


def response_with_headers(code, headers):
    codes = {
        200: 'HTTP/1.1 200 OK\r\n',
        404: 'HTTP/1.1 404 NOT FOUND\r\n',
        302: 'HTTP/1.1 302\r\n'
    }
    header = codes[code]
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header + '\r\n'


def validate_login(f):
    def vailedate(requests):
        u = obtain_user(requests)
        if len(u) > 0:
            form = {
                'ip': requests.ip
            }
            u[0].update(u[0].id, form)
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


def obtain_user(requests):
    cookies = requests.get('cookies')
    cookie = cookies.get('session_id', None)
    if cookie is None:
        cookie = cookies.get(' session_id')
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
    r = response_with_headers(302, headers) + '\r\n'
    return r.encode()


def template(name, **kwargs):
    path = 'htmls/{}.html'.format(name)
    with open(path, 'r', encoding='utf-8') as f:
        r = f.read()
    if len(kwargs) > 0:
        for k, v in kwargs.items():
            name = '{{' + str(k) + '}}'
            r = r.replace(name, kwargs[k])
    return r


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