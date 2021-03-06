from models.user import User
from uuid import uuid4
from routes import (
    error,
    redirect,
    cover,
    static,
    obtain_user,
    set_cookie,
    validate_login,
    response_with_headers,
    route,
)


@route('/api/login')
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
            ip_data = {
                'ip': str(requests.ip[0]),
            }
            User.update(u_id, ip_data)
            headers = {
                'Set-cookie': 'session_id={}; path=/; httponly=true;'.format(cookie_id),
            }
            set_cookie(cookie_id, u_id)
            return redirect('/', headers)
        else:
            return error(requests)
    else:
        return error(requests)


@route('/api/register')
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


@route('/api/quit')
def api_quit(_):
    headers = {
        'Set-cookie': 'session_id={}; path=/'.format('')
    }
    return redirect('/', headers)


@route('/api/add_head')
@validate_login
def api_cover(requests):
    if requests.get('method') == 'POST':
        u = obtain_user(requests)
        n = requests.get('file_headers').get('filename')
        cover_type = n.split('.')[1]
        if cover_type in ['jpg', 'png']:
            file_name = '{}.{}'.format(u.username, cover_type)

            path = 'covers/' + file_name
            data = requests.get('body')
            with open(path, 'wb') as f:
                f.write(data)
            form = {
                'head': file_name,
            }
            User.update(u.id, form)
        return redirect('/')
    else:
        return error(requests)


@route('/favicon.ico')
def api_favicon(_):
    headers = {
        'Content-Type': 'image/x-icon',
    }
    with open('favicon.ico', 'rb') as f:
        header = response_with_headers(200, headers)
        data = bytes(header, encoding="utf-8") + f.read()
        return data
