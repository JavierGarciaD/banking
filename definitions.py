import os


def root_dir():
    """
    :return: root folder path
    """
    return os.path.dirname(os.path.abspath(__file__))


def db_path():
    return os.path.join(root_dir(), "data", "forecast.sqlite")
