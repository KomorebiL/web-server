from models.user import User
from models.todo import Todo
from routes import (
    response_with_headers,
    obtain_user,
    error,
    redirect,
    validate_login,
    validate_login_redirect,
    validate_token,
    template,
    json_response,
    new_token,
)


@validate_login
def route_index(requests):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    token = new_token(requests)
    body = template('todo/index', token=token)
    data = header + body
    return data.encode(encoding='utf-8')


@validate_login
def api_all(requests):
    u = obtain_user(requests)
    if requests.get('method') == 'GET':
        form = {
            'user_id': u.id,
            'state': requests.get('query').get('state'),
        }
        ts = Todo.find(**form)
        data = [t.__dict__ for t in ts]
        return json_response(data)
    else:
        return error(requests)


@validate_token
def api_add(requests):
    u = obtain_user(requests)
    if requests.get('method') == 'POST':
        form = {
            'user_id': u.id,
            'content': requests.get('body').get('content')
        }
        t = Todo.new(form)
        data = {
            'content': t.get('content'),
            'id': t.get('id'),
            'token': new_token(requests),
        }
        return json_response(data)
    else:
        return error(requests)


@validate_token
def api_update(requests):
    u = obtain_user(requests)
    if requests.get('method') == 'POST':
        id = requests.get('body').get('id')
        state = requests.get('body').get('state')
        form = {
            'state': state,
        }
        Todo.update(id, u.id, form)
        data = {
            'token': new_token(requests)
        }
        return json_response(data)
    else:
        return error(requests)


@validate_token
def api_delete(requests):
    u = obtain_user(requests)
    if requests.get('method') == 'POST':
        form = {
            'user_id': u.id,
            'id': requests.get('body').get('id')
        }
        Todo.delete(**form)
        data = {
            'token': new_token(requests)
        }
        return json_response(data)
    else:
        return error(requests)


def route_dict():
    d = {
        '/todo': route_index,
        '/api/todo/add': api_add,
        '/api/todo/delete': api_delete,
        '/api/todo/all': api_all,
        '/api/todo/update': api_update,
    }
    return d
