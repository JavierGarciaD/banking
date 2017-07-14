import os


def root_dir():
    """
    :return: root folder path
    """
    return os.path.dirname(os.path.abspath(__file__))


def db_path(db_name):
    if db_name == 'forecast':
        return os.path.join(root_dir(), "data", "forecast.sqlite")
    else:
        return None
