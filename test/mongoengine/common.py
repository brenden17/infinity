from pymongo import Connection
import pandas as pd

class MetaMongoBase(type):
    pass


class Test(object):
    def __init__(self):
        pass

    def get_dataframe(self):
        conn = Connection()
        db = conn.yearlybalancedb
        year = db.year
        return DataFrame(list(year.find()))

