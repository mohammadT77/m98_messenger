from data_manager import DBManager
from core.models import User

manager = DBManager({'db_config':{
    'dbname':'eemjflhg',
    'host':'kesavan.db.elephantsql.com',
    'password':'17CkxoiUV7eQGqXLxXZGKstCpgBCE0rM',
    'user':'eemjflhg'
}})


print("All users:", *manager.read_all(User), sep='\n')



