# In the name of GOD
import datetime
from base import *
from db_manager import *
from config import config


cols_dict = {'_id': ('_id', 'SERIAL', 'PRIMARY KEY'), 'status': ('status', 'numeric', 'NOT NULL'),
             'date': ('date', 'DATE', 'NOT NULL')}  # """  """
print([" ".join(v) for v in cols_dict.values()])
sql_cols = ','.join([" ".join(v) for v in cols_dict.values()])
print(f"CREATE TABLE {'request'} ({sql_cols});", )

new_model_data = (1334, 200, datetime.datetime.now())
new_model_dict = dict(map(lambda item: (item[1], new_model_data[item[0]]), enumerate(cols_dict)))
new_model_str = ", ".join(map(lambda item: f"{item[1]} = {new_model_data[item[0]]}" if item[1] != '_id' else '', enumerate(cols_dict)))
new_model_str = new_model_str.lstrip(',')
print(f"{new_model_dict}")
print(f"{new_model_str}")

#
class Response(BaseModel):
    TABLE_NAME = "response"
    COLUMNS = {'status': ('status', 'numeric', 'NOT NULL'),
               'date': ('date', 'DATE', 'NOT NULL')}

    def __init__(self, status):
        self.status = status
        self.date = datetime.datetime.now()



my_database_manager = DBManager({'db_config': config('requirements.ini', "postgresql")})

new_response = Response(404)
# print(Response.mro())
new_response_id = my_database_manager.create(new_response)
# new_response_loaded = my_database_manager.read(new_response_id, Response)
# print(new_response_loaded)
# print(new_response_loaded.status)
# print(new_response_loaded.date)
# print(new_response_loaded._id)
# print(new_response._id)
# print(new_response_loaded._id == new_response._id)
#
#
# for response in my_database_manager.read_all(Response):
#     print(response, response.status, response.date)

print(new_response, new_response.status, new_response.date)
new_response.status = 500
my_database_manager.update(new_response)
new_response_loaded = my_database_manager.read(new_response_id, Response)
print(new_response_loaded, new_response_loaded.status, new_response_loaded.date)
my_database_manager.delete(15, Response)
print(my_database_manager.read(15, Response))


# my_database_manager.truncate(Response)