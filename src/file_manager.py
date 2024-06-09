from abc import ABC, abstractmethod
import os
import os.path
import json
from src.vacancies import Vacancy

ROOT_DIR = os.getcwd()
class DataManager:

    @abstractmethod
    def __init__(self, file_name):
        pass

    @abstractmethod
    def save_data(self, data):
        pass

    @abstractmethod
    def add_vacancy(self, data):
        pass

    @abstractmethod
    def get_vacancy(self, params):
        pass

    @abstractmethod
    def delete_vacancy(self, data):
        pass


class FileManager(DataManager):

    def __init__(self, file_name):
        self.file_name = file_name
        #ROOT_DIR = os.getcwd() #путь к директории проекта
        path_data = os.path.join(ROOT_DIR, 'data') #составляем путь к папке данных и при её отсутствии создаем
        if not os.path.exists(path_data):
            os.mkdir('data')
        path = os.path.join(ROOT_DIR, 'data', file_name)
        self.path = path
        with open(self.path, mode='w', encoding='utf-8') as data_file:
            pass

    def save_data(self, data: list[Vacancy]):
        data_to_write = []
        with (open(self.path, 'w', encoding='utf-8') as data_file):
            for item in data:
                item_in_dict = item.format_instance_to_dict()
                data_to_write.append(item_in_dict)
            json.dump(data_to_write, data_file, ensure_ascii=False)

    def read_data(self):
        with (open(self.path, 'r', encoding='utf-8') as data_file):
            return json.load(data_file)

    def write_data(self, vacancies: list[dict]):
        with open(self.path, 'w', encoding='utf-8') as data_file:
            json.dump(vacancies, data_file, ensure_ascii=False)

    def add_vacancy(self, vacancy):
        vacancies = self.read_data()
        vacancy.format_instance_to_dict()
        vacancies.append(vacancy.format_instance_to_dict())
        self.write_data(vacancies)


    def get_vacancy(self, params):
        with open(self.path, 'w+', encoding='utf-8') as data_file:
            pass

