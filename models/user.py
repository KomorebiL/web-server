from models import Model


class User(Model):
    @classmethod
    def valid_names(cls):
        names = [
            # (字段名, 类型, 默认值)
            ('username', str, ''),
            ('password', str, ''),
            ('cookie', str, ''),
            ('head', str, '1.jpg')
        ]
        return names

    @classmethod
    def validate_login(cls, **kwargs):
        username = kwargs.get('username')
        data = cls.find(username=username)
        if len(data) > 0:
            u = data[0]
            p = u.get('password')
            return p == kwargs['password']
        else:
            return False
