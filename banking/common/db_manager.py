from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import select
import definitions
from sys import getsizeof


def forecast_db():
    """
    Standard conection to forecast database
    :return: connection, metadata
    """
    # Create engine
    db_path = r"sqlite:///" + definitions.db_path()
    engine = create_engine(db_path, echo = False)

    # get connection and metadata
    conn = engine.connect()
    meta = MetaData(engine, reflect = True)

    return conn, meta


def get_contract_info(product_name):
    """
    Get contract info from forecast database
    :return: dict with nper, rate_type, repricing for a given product
    """
    db = forecast_db()
    conn = db[0]
    meta = db[1]
    contract_info = meta.tables['contract_info']

    # Construct select sql statement
    sql_query = select([contract_info]).where(
            contract_info.c.product_name == product_name)

    # execute and fetch result
    ans = conn.execute(sql_query)
    row = ans.fetchone()

    # Close the connection
    ans.close()
    conn.close()

    # Construct dictionary
    return dict(nper = row[1],
                rate_type = row[2],
                repricing = row[3])


if __name__ == '__main__':

    x = get_contract_info('tarjeta de credito')

    print(x)
