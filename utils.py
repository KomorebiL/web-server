def template(name):
    path = 'htmls/{}.html'.format(name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
