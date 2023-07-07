# In the name of GOD
from typing import Dict
from configparser import ConfigParser


def config(filename="requirements.ini", section="postgresql") -> Dict:
    """ Reads config parameters from specified file and makes a dictionary of that """
    db = {}
    parser = ConfigParser()
    parser.read(filename)
    print(parser.has_section(section))
    print(parser.items(section))
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'section {section} is not found in the file {filename}')
    return db


config()
