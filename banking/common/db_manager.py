import numpy as np
import io
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from definitions import db_path


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

