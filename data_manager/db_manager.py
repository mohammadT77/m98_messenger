from .base import BaseManager, BaseModel
import psycopg2 as pg


class DBManager(BaseManager):
    
    def __init__(self, config: dict) -> None:
        super().__init__(config)  # {'db_config':{'dbname':'', 'host':'', 'password':'', 'user':'', ...}}
        self._db_config = config['db_config']
        self.__conn = pg.connect(**self._db_config)

    @staticmethod
    def converter_model_to_query(value):
        if isinstance(value, str):
            return f"'{value}'"
        elif value is None:
            return 'NULL'
        else:
            return f"'{str(value)}'"
    
    def create_table(self, model_cls: type):
        """


        {'_id': ('_id', 'SERIAL', 'PRIMARY KEY'),}

        """
        assert issubclass(model_cls, BaseModel)

        with self.__conn.cursor() as curs:
            cols_dict = model_cls._get_columns() # """  """
            sql_cols = ','.join([" ".join(v) for v in cols_dict.values()])
            curs.execute(f"CREATE TABLE {model_cls.TABLE_NAME} ({sql_cols});", )
        
        self.__conn.commit()
    
    def _check_table_exists(self,  model_cls: type):
        with self.__conn.cursor() as curs:
            curs.execute("SELECT * FROM information_schema.tables WHERE table_name=%s",
                        (model_cls.TABLE_NAME,))
            return bool(curs.fetchone())

    def create(self, m: BaseModel):
        if not self._check_table_exists(m.__class__):
            self.create_table(m.__class__)
        
        model_data = m.to_dict()  # {'_id':1, 'username':'akbar', ...}
        converter = self.converter_model_to_query

        with self.__conn.cursor() as curs:
            keys = ','.join(model_data.keys())
            values = ','.join(map(converter, model_data.values())) # 1, 'akbar', 'akbar1',... -> 1, 'akbar', 'akbar1' -> "1, 'akbar', 'akbar1'"
            curs.execute(f"INSERT INTO {m.TABLE_NAME} ({keys}) VALUES ({values}) RETURNING _id;")
            new_model_id = curs.fetchone()
            m._id = new_model_id[0]
        
        self.__conn.commit()
        return new_model_id[0]

    def read(self, id: int, model_cls: type) -> BaseModel:
        keys_dict = enumerate(model_cls._get_columns())
        with self.__conn.cursor() as curs:
            curs.execute(f"SELECT * FROM {model_cls.TABLE_NAME} WHERE  _id = %s ;", (id, ))
            new_model_data = curs.fetchone()
            model_obj = None
            if new_model_data:
                new_model_dict = dict(map(lambda item: (item[1], new_model_data[item[0]]), keys_dict))
                model_obj = model_cls.from_dict(new_model_dict)
        self.__conn.commit()
        return model_obj

    def update(self, model: BaseModel) -> None:
        assert hasattr(model, '_id'), "model must have _id"
        model_data = model.to_dict()  # {'_id':1, 'username':'akbar', ...}
        model_data.pop('_id')
        converter = self.converter_model_to_query

        with self.__conn.cursor() as curs:
            keys = model_data.keys()
            values = list(map(converter, model_data.values()))  # 1, 'akbar', 'akbar1',... -> 1, 'akbar', 'akbar1' -> "1, 'akbar', 'akbar1'"
            new_model_str = " , ".join(map(lambda item: f"{item[1]} = {values[item[0]]}", enumerate(keys)))
            curs.execute(f"UPDATE {model.TABLE_NAME} SET {new_model_str} WHERE _id = {converter(model._id)};")
        self.__conn.commit()

    def delete(self, id: int, model_cls: type) -> None:
        with self.__conn.cursor() as curs:
            curs.execute(f"DELETE FROM {model_cls.TABLE_NAME} WHERE  _id = {id};")
        self.__conn.commit()

    def read_all(self, model_cls: type):
        assert issubclass(model_cls, BaseModel)
        assert getattr(model_cls, "TABLE NAME", None) , "Could not find Table Name"
        with self.__conn.cursor() as curs:
            curs.execute(f"SELECT * FROM {model_cls.TABLE_NAME};")
            new_models_data = curs.fetchall()
        self.__conn.commit()
        for new_model_data in new_models_data:
            keys_dict = enumerate(model_cls._get_columns())
            new_model_dict = dict(map(lambda item: (item[1], new_model_data[item[0]]), keys_dict))
            model_obj = model_cls.from_dict(new_model_dict)
            yield model_obj

    def truncate(self, model_cls: type) -> None:
        assert issubclass(model_cls, BaseModel), "Model should inherit from BasemModel"
        assert getattr(model_cls, 'TABLENAME', None), "Could not find TABLE NAME"
        with self.__conn.cursor() as curs:
            curs.execute(f"DELETE FROM {model_cls.TABLE_NAME};")
        self.__conn.commit()

    def raw_query(self, query: str):
        with self.__conn.cursor() as curs:
            curs.execute(query)
            data = curs.fetchall()
        self.__conn.commit()
        return data


    
    
