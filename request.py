class Request:
    def __init__(self, r):
        self.method = ''
        self.body = {}
        self.path = ''
        self.query = {}
        self.cookies = {}
        self.headers = {}
        self.file_headers = {}
        self.form(r)

    def get(self, name):
        return self.__dict__.get(name)

    def form(self, r):
        header, body = self._split(r)
        r_line, *head = header.split('\r\n')
        self._headers(head)
        self._respond(r_line)
        self._cookie()
        self._body(body)
        return self.__dict__

    def _split(self, r):
        i = 4
        while i < len(r):
            if r[i - 4: i] == b'\r\n\r\n':
                break
            i += 1
        header, body = r[:i - 4].decode('utf-8'), r[i:]
        return header, body

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

    def _body(self, body):
        if len(body) <= 0:
            self.body = {}
        else:
            type_ = self.headers.get('Content-Type')
            if type_[:20] != ' multipart/form-data':
                args = body.split('&')
                query = {}
                for arg in args:
                    k, v = arg.split('=')
                    query[k] = v
                self.body = query
            else:
                file_header, file_body = self._split(body)
                self._file_header(file_header)
                self.body = file_body

    def _file_header(self, headers):
        headers = headers.split('\r\n')[1].split(';')
        flag = 0
        for h in headers:
            if h.find(':') is not -1:
                flag = 1
            elif h.find('=') is not -1:
                flag = 2

            if flag is 1:
                k, v = h.split(':')
                self.file_headers[k] = v
            elif flag is 2:
                k, v = h.split('=')
                k = k[1:]
                v = v[:-1]
                self.file_headers[k] = v

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
