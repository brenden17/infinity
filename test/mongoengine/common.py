'''
mongoengine - http://mongoengine-odm.readthedocs.org/en/latest/#
pymongo - http://api.mongodb.org/python/current/
'''

from pymongo import Connection, database
import mongoengine
import pandas as pd

def convertname(name):
    newname = [name[0].lower()]
    A, Z = ord('A')-1, ord('Z')-1
    for c in name[1:]:
        if A < ord(c) < Z:
            c = '_' + c.lower()
        newname.append(c)
    return ''.join(newname)


class MongoHelper(object):
    @staticmethod
    def get_dbs():
        conn = Connection()
        return conn.database_names()

    @staticmethod
    def drop_db(dbname):
        conn = Connection()
        return conn.drop_database(dbname)

    @staticmethod
    def get_collections(dbname):
        try:
            conn = Connection()
            db = database.Database(conn, dbname)
            return db.collection_names()
        except Exception as e:
            print(str(e))

    @staticmethod
    def drop_collections(dbname, collection_name):
        try:
            conn = Connection()
            db = database.Database(conn, dbname)
            return db.drop_collection(collection_name)
        except Exception as e:
            print(str(e))

    @staticmethod
    def get_collection(dbname, collection_name):
       try:
           conn = Connection()
           db = database.Database(conn, dbname)
           return db[collection_name]
       except Exception as e:
           print(str(e))

    @staticmethod
    def get_dataframe(dbname, collection_name, option={}):
       try:
           c = MongoHelper.get_collection(dbname, collection_name)
           return pd.DataFrame(list(c.find(**option)))
       except Exception as e:
           print(str(e))

    @staticmethod
    def collection2dataframe(collection, option={}):
        dbname = collection._meta.get('db_alisa') or mongoengine.connect.__globals__['_connection_settings']['default']['name']
        cname = collection._meta.get('collection')
        cname = convertname(cname)
        return MongoHelper.get_dataframe(dbname, cname, option)

    @staticmethod
    def collection2array(collection, option={}):
        return MongoHelper.collection2dataframe(collection, option).values


'''
support with metaclass
'''
class MetaMongoBase(type):
    def __new__(meta, classname, supers, classdict):
        if 'mongometa'in classdict:
            mongometa = classdict['mongometa']
            dbname = mongometa.get('dbname', None)
            o = mongometa.get('option', {})
            collection = convertname(classname)
            classdict['get_dataframe'] = lambda self:MongoHelper.get_dataframe(dbname, collection, o)
        return type.__new__(meta, classname, supers, classdict)

class MongoBase(object):
    __metaclass__ = MetaMongoBase
    def __init__(self):
        pass

class Year(MongoBase):
    mongometa = {'dbname':'yearlybalancedb', 'option':{'field':['dayat']}}
    #mongometa = {'dbname':'yearlybalancedb'}
    def __init__(self):
        pass

if __name__ == '__main__':
    y = Year()
    print(y.get_dataframe())

    df = MongoHelper.get_dataframe('yearlybalancedb','daily_balance',{'field':['dayat']})
    print(df.values)
