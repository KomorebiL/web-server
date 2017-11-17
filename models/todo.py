from models import Model
from bson import ObjectId


class Todo(Model):
    @classmethod
    def valid_names(cls):
        names = [
            # (字段名, 类型, 默认值)
            ('user_id', str, ''),
            ('content', str, ''),
            ('state', str, 'todo'),
        ]
        return names

    @classmethod
    def delete(cls, id, user_id):
        name = cls.__name__
        query = {
            '_id': ObjectId(id),
            'user_id': user_id,
        }
        cls.db[name].remove(query)

    @classmethod
    def update(cls, id, user_id, form):
        name = cls.__name__
        t = Todo.find(id=ObjectId(id))[0]
        if t.user_id == user_id:
            query = {
                '_id': ObjectId(id)
            }
            values = {
                '$set': form,
            }
            cls.db[name].update_one(query, values)
