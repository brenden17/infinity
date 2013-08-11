from pymongo import Connection, database
import pandas as pd

class MongoHelper(object):
    def __init__(self):
        pass

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

class MetaMongoBase(type):
    def __new__(meta, classname, supers, classdict):
        if 'mongometa'in classdict:
            mongometa = classdict['mongometa']
            dbname = mongometa.get('dbname', None)
            collection = classname.lower()
            classdict['get_dataframe'] = lambda self,o:MongoHelper.get_dataframe(dbname, collection, o)
        return type.__new__(meta, classname, supers, classdict)

class MongoBase(object):
    __metaclass__ = MetaMongoBase
    def __init__(self):
        pass

class Year(MongoBase):
    mongometa = {'dbname':'yearlybalancedb'}
    def __init__(self):
        pass

if __name__ == '__main__':
    y = Year()
    print(y.get_dataframe({}))

    df = MongoHelper.get_dataframe('yearlybalancedb','daily_balance',{'field':['dayat']})
    print(df.values)
