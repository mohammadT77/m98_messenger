from typing import Generator, Any 
from .base import BaseModel, BaseManager
import pickle
import os

class FileManager(BaseManager):
    ROOT_PATH_CONFIG_KEY = 'ROOT_PATH'

    def __init__(self, config: dict) -> None:
        assert self.ROOT_PATH_CONFIG_KEY in config.keys(), "Provide a config"
        super().__init__(config)
    
    @property
    def files_root(self):
        root_dir = self.config[self.ROOT_PATH_CONFIG_KEY]  # data/
        if not os.path.exists(root_dir):  # does not exist: 'data/'
            os.mkdir(root_dir)  # mkdir data/
        return root_dir

    def _get_id(self, model_type: type) -> int: # User
        files = os.listdir(self.files_root+'/')
        ids = []
        for f in files:
            if f.startswith(model_type.__name__):
                ids.append(int(f.split('_')[-1].split('.')[0]))
        return max(ids)+1 if ids else 1

    def _get_file_path(self, _id, model_type: type) -> str: # Event id = 24 -> "data/Event_24.pkl"
        return f"{self.files_root}/{model_type.__name__}_{_id}.pkl".replace('//', '/')  

    def create(self, model: BaseModel) -> Any:
        # Set ID
        model._id = self._get_id(model.__class__)

        # Get path
        path = self._get_file_path(model._id, model.__class__)

        # Store in file
        with open(path, 'wb') as f:
            pickle.dump(model, f)
        return path
        
    def read(self, id: int, model_cls: type) -> BaseModel:
        # Get path
        path = self._get_file_path(id, model_cls)

        # Read content
        with open(path, 'rb') as f:
            model = pickle.load(f)
            return model # isinstance(model, Event) -> True

    def update(self, model: BaseModel) -> None:
        assert hasattr(model, '_id'), "model must have _id"
        path = self._get_file_path(model._id, model.__class__)  # model._id = None -> data/Event_None.pkl
        with open(path, 'wb') as f:
            pickle.dump(model, f)

    def delete(self, id: int, model_cls: type) -> None:
        # Get path
        path = self._get_file_path(id, model_cls)

        # Remove the file
        if os.path.exists(path):
            os.remove(path)

    def read_all(self, model_cls: type = None) -> Generator:  # data/Event_1.pkl
        for file_name in os.listdir(self.files_root):
            if not file_name.endswith('.pkl'):
                continue
            if model_cls and not file_name.startswith(model_cls.__name__): # Need fix
                continue
            file_path = os.path.join(self.files_root, file_name)  # data, Event_2.pkl -> data/Event_2.pkl
            with open(file_path, 'rb') as f:
                instance = pickle.load(f)
                yield instance

    def truncate(self, model_cls: type) -> None:
        for model in self.read_all(model_cls):
            self.delete(model._id, model.__class__)

