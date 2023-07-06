from data_manager.file_manager import FileManager, BaseModel
from unittest import TestCase, main
import os
import shutil


class TestModel(BaseModel):
    pass


class FileManagerTest(TestCase):
    test_root_dir = 'test_data/'
    manager = FileManager({'ROOT_PATH': test_root_dir})
    
    def tearDown(self) -> None: # after
        if os.path.exists(self.test_root_dir):
            shutil.rmtree(self.test_root_dir)

    def test1_create(self):
        model1 = TestModel()
        self.assertFalse(hasattr(model1, '_id'))
        self.manager.create(model1)
        self.assertTrue(hasattr(model1, '_id'))



if __name__ == '__main__':
    main()