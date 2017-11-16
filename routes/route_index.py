from models.user import User
from routes import (
    response_with_headers,
    obtain_user,
    error,
    redirect,
    validate_login,
    template,
    validate_login_redirect,
)


@validate_login
def route_index(requests):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    u = obtain_user(requests)[0]
    body = template('index', username=u.username, head=u.head, ip=u.ip)
    data = header + body
    return data.encode(encoding='utf-8')


@validate_login_redirect
def route_login(requests):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    body = template('login')
    data = header + body
    return data.encode(encoding='utf-8')


@validate_login_redirect
def route_register(requests):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    body = template('register')
    data = header + body
    return data.encode(encoding='utf-8')


def route_dict():
    d = {
        '/': route_index,
        '/login': route_login,
        '/register': route_register,
    }
    return d
