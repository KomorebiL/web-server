from models.user import User
from routes import (
    response_with_headers,
    obtain_user,
    error,
    redirect,
    validate_login,
    template,
    validate_login_redirect,
    route,
)


@route('/')
@validate_login
def route_index(requests):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    u = obtain_user(requests)
    body = template('index', username=u.username, head=u.head, ip=u.ip)
    data = header + body
    return data.encode(encoding='utf-8')


@route('/login')
@validate_login_redirect
def route_login(_):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    body = template('login')
    data = header + body
    return data.encode(encoding='utf-8')


@route('/register')
@validate_login_redirect
def route_register(_):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    body = template('register')
    data = header + body
    return data.encode(encoding='utf-8')
