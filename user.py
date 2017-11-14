from model import Model


class User(Model):
    @classmethod
    def valid_names(cls):
        names = [
            # (字段名, 类型, 默认值)
            ('user', str, ''),
            ('pass', str, ''),
        ]
        return names