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


def api_chatroom(requests):
    print(requests)
    return json_response('')


def route_dict():
    d = {
        '/api/chatroom': api_chatroom,
    }
    return d
