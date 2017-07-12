from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import select
import definitions


def get_contract_info(product_name):
    """
    Get contract info from forecast database
    :return: dict with nper, rate_type, repricing for a given product
    """
    # Create engine
    db_path = r"sqlite:///" + definitions.db_path()
    engine = create_engine(db_path, echo = False)

    # Create connection
    conn = engine.connect()

    meta = MetaData(engine, reflect = True)
    table = meta.tables['contract_info']

    # Select
    select_st = select([table]).where(
            table.c.product_name == product_name)

    ans = conn.execute(select_st).fetchall()

    # Close the connection
    conn.close()

    return dict(nper = ans[0][1],
                rate_type = ans[0][2],
                repricing = ans[0][3])


if __name__ == '__main__':

    x = get_contract_info('tarjeta de credito')

    print(x)
