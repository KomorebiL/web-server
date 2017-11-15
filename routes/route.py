from models.user import User
from utils import template
from routes import (
    response_with_headers,
    obtain_user,
    error,
    redirect,
    validate_login,
)


@validate_login
def route_index(requests):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    u = obtain_user(requests)[0]
    body = '<h1>Hello {}!</h1>'.format(u.username)
    data = header + '\r\n\r\n' + body
    return data.encode(encoding='utf-8')


def route_login(requests):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    body = template('login')
    data = header + '\r\n' + body
    return data.encode(encoding='utf-8')


def route_register(requests):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    body = template('register')
    data = header + '\r\n' + body
    return data.encode(encoding='utf-8')


def route_dict():
    d = {
        '/': route_index,
        '/login': route_login,
        '/register': route_register,
    }
    return d
