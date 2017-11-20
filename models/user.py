from models import Model
import hashlib
from bson import ObjectId


class User(Model):
    @classmethod
    def valid_names(cls):
        names = [
            # (字段名, 类型, 默认值)
            ('username', str, ''),
            ('password', str, ''),
            ('head', str, '1.jpg'),
        ]
        return names

    @classmethod
    def new(cls, form):
        m = cls()
        form['password'] = cls.password_salt(form['password'])
        for name in cls.valid_names():
            n, f, v = name
            if n in form:
                setattr(m, n, f(form[n]))
            else:
                setattr(m, n, v)
        m.save()
        return m.__dict__

    @classmethod
    def find(cls, **kwargs):
        name = cls.__name__
        p = kwargs.get('password', None)
        if p is not None:
            kwargs['password'] = cls.password_salt(p)
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')
        datas = cls.db[name].find(kwargs)
        l = [cls._new_data(d) for d in datas]
        return l

    @staticmethod
    def password_salt(password, salt='komorebi!@#$'):
        def sha256(s):
            return hashlib.sha256(s.encode('utf-8')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @classmethod
    def validate_login(cls, **kwargs):
        username = kwargs.get('username')
        data = cls.find(username=username)
        if len(data) > 0:
            u = data[0]
            p = u.get('password')
            return p == cls.password_salt(kwargs['password'])
        else:
            return False
