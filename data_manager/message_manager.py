from data_manager import BaseModel
import psycopg2 as pg



class MessageManager(BaseModel):
    
    def __init__(self, config) -> None:
        super().__init__(config)
        self.msg_config = config["msg_data"]
        self.__dbmanager = self.msg_config['dbmanager']

    def create_message(self):
        pass

    @classmethod
    def inbox(cls):
        pass

    def sent_box(self):
        pass