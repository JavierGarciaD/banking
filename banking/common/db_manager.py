from sqlalchemy import create_engine
from sqlalchemy import MetaData
from definitions import db_path
from sqlalchemy.exc import SQLAlchemyError


def forecast_db():
    """
    Conection to forecast database
    :return: connection, metadata
    """
    # Create engine
    db = r"sqlite:///" + db_path()
    engine = create_engine(db, echo = False)

    # get connection and metadata
    conn = engine.connect()
    meta = MetaData(engine, reflect = True)

    return conn, meta


class DB:

    # TODO https://stackoverflow.com/a/19440352/3512107
    # TODO Manage connections to database

    def __init__(self):
        self.conn = None
        self.meta = None
        self.engine = None

    def db_engine(self):
        db = r"sqlite:///" + db_path()
        self.engine = create_engine(db, echo = False)

    def connect(self):
        try:
            self.conn = self.engine.connect()
        except (SQLAlchemyError, AttributeError):
            self.db_engine()
            self.conn = self.engine.connect()

    def query(self, sql):
        try:
            ans = self.conn.execute(sql)
        except (SQLAlchemyError, AttributeError):
            self.connect()
            ans = self.conn.execute(sql)
        return ans

    def metadata(self):
        try:
            meta = MetaData(self.engine, reflect = True)
        except (SQLAlchemyError, AttributeError):
            self.db_engine()
            meta = MetaData(self.engine, reflect = True)
        return meta


if __name__ == '__main__':

    db = DB()

    sql = "SELECT score FROM scores"
    cur = db.query(sql)
    meta = db.metadata
    for x in cur:
        print(x)

    print(meta)
