from models.user import User
from uuid import uuid4
from utils import *
from routes import (
    error,
    redirect,
)


def api_login(requests):
    if requests.get('method') == 'POST':
        b = requests.body
        user_data = {
            'username': b.get('username'),
            'password': b.get('password'),
        }
        if User.validate_login(**user_data):
            u_id = User.find(**user_data)[0].id
            cookie_id = str(uuid4())
            cookie_data = {
                'cookie': cookie_id,
            }
            User.update(u_id, cookie_data)
            headers = {
                'Set-cookie': 'session_id={}; path=/'.format(cookie_id)
            }
            return redirect('/', headers)
        else:
            return error(requests)
    else:
        return error(requests)


def api_register(requests):
    if requests.get('method') == 'POST':
        b = requests.body
        user_data = {
            'username': b.get('username'),
            'password': b.get('password'),
        }
        User.new(user_data)
        return redirect('/login')
    else:
        return error(requests)


def route_dict():
    d = {
        '/api/login': api_login,
        '/api/register': api_register,
    }
    return d
