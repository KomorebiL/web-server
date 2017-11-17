from models.user import User
from models.todo import Todo
from routes import (
    response_with_headers,
    obtain_user,
    error,
    redirect,
    validate_login,
    template,
    validate_login_redirect,
    json_response,
)


@validate_login
def route_index(requests):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(200, headers)
    body = template('todo/index')
    data = header + body
    return data.encode(encoding='utf-8')


@validate_login
def api_all(requests):
    u = obtain_user(requests)[0]
    if requests.get('method') == 'POST':
        print(requests)
        form = {
            'user_id': u.id,
            'state': requests.get('body').get('state'),
        }
        ts = Todo.find(**form)
        data = [t.__dict__ for t in ts]
        return json_response(data)
    else:
        return error(requests)


@validate_login
def api_add(requests):
    u = obtain_user(requests)[0]
    if requests.get('method') == 'POST':
        form = {
            'user_id': u.id,
            'content': requests.get('body').get('content')
        }
        t = Todo.new(form)
        data = {
            'content': t.get('content'),
            'state': t.get('state'),
        }
        return json_response(data)
    else:
        return error(requests)


@validate_login
def api_update(requests):
    u = obtain_user(requests)[0]
    if requests.get('method') == 'POST':
        id = requests.get('body').get('id')
        state = requests.get('body').get('state')
        form = {
            'state': state,
        }
        Todo.update(id, u.id, form)
    else:
        return error(requests)


@validate_login
def api_delete(requests):
    u = obtain_user(requests)[0]
    if requests.get('method') == 'POST':
        form = {
            'userid': u.id,
            'id': requests.get('body').get('delete')
        }
        Todo.delete(**form)
    else:
        return error(requests)


def route_dict():
    d = {
        '/todo': route_index,
        '/api/todo/add': api_add,
        '/api/todo/delete': api_delete,
        '/api/todo/all': api_all,
    }
    return d
