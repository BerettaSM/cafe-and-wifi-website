import inspect
import sys
from datetime import datetime


def formatted_timestamp():
    # return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(datetime.utcnow())


def to_bool(yes_no: str) -> bool:
    return yes_no == 'True'


def does_class_exist_in_models(cls):
    """
    This function checks if a particular class exists
    inside the 'models' module. This function will
    include imported classes inside the module into
    the check.

    :param cls: A class to check for.
    :return: True if class name exists inside module + imports, False otherwise.
    """
    from .models import __name__ as name
    cls_members = inspect.getmembers(sys.modules[name], inspect.isclass)
    cls_names = [item[1].__name__ for item in cls_members]
    return cls.__name__ in cls_names
