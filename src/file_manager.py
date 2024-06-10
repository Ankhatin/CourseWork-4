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
    def read_data(self, data):
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
        if self.check_on_exist(self.file_name):
            self.path = os.path.join(ROOT_DIR, 'data', file_name)
        else:
            path_data = os.path.join(ROOT_DIR, 'data') # Составляем путь к папке данных и при её отсутствии создаем
            if not os.path.exists(path_data):
                os.mkdir('data')
            path = os.path.join(ROOT_DIR, 'data', file_name)
            self.path = path

    def save_data(self, data: list[Vacancy]):
        '''
        Функция принимает список экземпляров вакансий, преобразует их в словарь
        и в формате json записывает в файл
        '''
        data_to_write = []
        with (open(self.path, 'w', encoding='utf-8') as data_file):
            for item in data:
                item_in_dict = item.format_instance_to_dict()
                data_to_write.append(item_in_dict)
            json.dump(data_to_write, data_file, ensure_ascii=False)

    def read_data(self):
        with (open(self.path, 'r', encoding='utf-8') as data_file):
            data = json.load(data_file)
            vacancies : list[Vacancy] = []
            for item in data:
                vacancy = Vacancy(item['name'], item['url'], item['salary_from'], item['salary_to'],
                                  item['salary'], item['currency'], item['experience'], item['date'])
                vacancies.append(vacancy)
            return vacancies

    def write_vacancy(self, vacancies: list[dict]):
        with open(self.path, 'w', encoding='utf-8') as data_file:
            json.dump(vacancies, data_file, ensure_ascii=False)

    def add_vacancy(self, vacancy):
        vacancies = self.read_data()
        vacancies.append(vacancy)
        self.save_data(vacancies)

    def get_vacancy(self, **kwargs):
        '''
        Функция принимает произвольное количество именованных переменных,
        имена должны совпадать со свойствами экземпляров вакансий,
        возвращает экземпляр найденной вакансии
        '''
        if len(kwargs) == 0:
            print('Параметры для поиска вакансии не заданы')
        else: # Если переданы именованные аргументы
            if kwargs.get('name'):
                name = kwargs['name']
            if kwargs.get('salary_from'):
                salary_from = kwargs['salary_from']
            if kwargs.get('salary_to'):
                salary_to = kwargs['salary_to']
            vacancies = self.read_data()
            for vacancy in vacancies:
                if 'name' in locals() and vacancy.name.lower() == name.lower():
                    if 'salary_from' in locals() and vacancy.salary_from == salary_from:
                        if 'salary_to' in locals() and vacancy.salary_to == salary_to:
                            return vacancy
        return False

    def delete_vacancy(self, vacancy):
        vacancies = self.read_data()
        vacancies.remove(vacancy)
        self.save_data(vacancies)

    @staticmethod
    def check_on_exist(file_name):
        path_data = os.path.join(ROOT_DIR, 'data', file_name)
        try:
            with open(path_data, mode='r', encoding='utf-8') as f:
                pass
            return True
        except FileNotFoundError:
            return False
