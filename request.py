class request:
    def __init__(self, header):
        self.method = ''
        self.body = ''
        self.path = ''
        self.query = {}
        self.form(header)

    def get(self, name):
        return self.__dict__.get(name)

    def form(self, header):
        analyze = self._body(header).split('\r\n')
        r_line, head = analyze[0], analyze[1:]
        self._respond(r_line)
        # for h in head:
        #     analyze = h.split(':', 1)
        #     key, value = analyze[0], analyze[1]
        #     self.__dict__[key] = value
        return self.__dict__

    def _respond(self, respond_line):
        data = respond_line.split()
        self.method = data[0]
        self._path_and_query(data[1])

    def _body(self, header):
        header, body = header.split('\r\n\r\n', 1)
        self.body = body
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
        return str(self.__dict__)
