from pymongo import MongoClient
from bson import ObjectId


class Model:
    db = MongoClient()['komorebi']

    def save(self):
        name = self.__class__.__name__
        _id = self.db[name].save(self.__dict__)
        self.id = str(_id)

    @classmethod
    def new(cls, form):
        m = cls()
        for name in cls.valid_names():
            n, f, v = name
            if n in form:
                setattr(m, n, f(form[n]))
        m.save()

    @classmethod
    def delete(cls, id):
        name = cls.__name__
        query = {
            '_id': ObjectId(id),
        }
        cls.db[name].remove(query)

    @classmethod
    def update(cls, id, form):
        name = cls.__name__
        query = {
            '_id': ObjectId(id)
        }
        values = {
            '$set': form,
        }
        cls.db[name].update_one(query, values)

    @classmethod
    def find(cls, **kwargs):
        name = cls.__name__
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')
        datas = cls.db[name].find(kwargs)
        l = [cls._new_data(d) for d in datas]
        return l

    @classmethod
    def _new_data(cls, bson):
        m = cls()
        for key in bson:
            setattr(m, key, bson[key])
        m.id = str(bson['_id'])
        return m

    @classmethod
    def all(cls):
        return cls.find()

    def __repr__(self):
        lt = ['{} = {}'.format(k, v) for k, v in self.__dict__.items()]
        return '\n<\n{}\n>'.format('\n'.join(lt))
