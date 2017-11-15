import request
from models.user import User


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
    return header


def validate_login(f):
    def vailedate(requests):
        u = obtain_user(requests)
        if len(u) > 0:
            return f(requests)
        else:
            return redirect('/login')
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
