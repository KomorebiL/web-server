class request:
    def __init__(self, header):
        self.method = ''
        self.body = ''
        self.path = ''
        self.query = {}
        self.cookies = {}
        self.headers = {}
        self.form(header)

    def get(self, name):
        return self.__dict__.get(name)

    def form(self, header):
        r_line, *head = self._body(header).split('\r\n')
        self._headers(head)
        self._respond(r_line)
        self._cookie()
        return self.__dict__

    def _headers(self, header):
        for h in header:
            key, value = h.split(':', 1)
            self.headers[key] = value

    def _cookie(self):
        cookies = self.headers.get('Cookie', None)
        if cookies is not None:
            cs = cookies.split('; ')
            for c in cs:
                if '=' in c:
                    k, v = c.split('=', 1)
                    self.cookies[k] = v

    def _respond(self, respond_line):
        data = respond_line.split()
        self.method = data[0]
        self._path_and_query(data[1])

    def _body(self, header):
        header, body = header.split('\r\n\r\n', 1)
        if len(body) <= 0:
            self.body = body
        else:
            args = body.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=')
                query[k] = v
            self.body = query
        return header

    def _path_and_query(self, header):
        index = header.find('?')
        if index == -1:
            self.path = header
            self.query = {}
        else:
            path, args = header.split('?', 1)
            args = args.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=')
                query[k] = v
            self.path = path
            self.query = query

    def __repr__(self):
        string = ''
        for k, v in self.__dict__.items():
            string += '{}: {}\n'.format(k, v)
        return string
