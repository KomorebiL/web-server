import request


def response_for_path(r):
    requests = request.request(r)
    path = requests.get('path')
    routes = {
        '/': route_index,
    }
    route = routes.get(path, route_error)
    return route(requests)


def route_error(requests):
    code = b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'
    return code


def route_index(requests):
    query = requests.get('query')
    header = 'HTTP/1.1 200 OK'

    if len(query) > 0 and 'name' in query:
        body = '<h1>Hello World {}!</h1>'.format(query['name'])
    else:
        body = '<h1>Hello World!</h1>'

    data = header + '\r\n\r\n' + body
    return data.encode(encoding='utf-8')
