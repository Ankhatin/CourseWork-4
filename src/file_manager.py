from abc import ABC, abstractmethod
import os
import os.path
import json
from src.vacancies import Vacancy
from main import ROOT_DIR


class DataManager(ABC):

    @abstractmethod
    def __init__(self, file_name):
        pass

    @abstractmethod
    def save_data(self, data):
        pass

    @abstractmethod
    def read_data(self):
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
        '''
        Функция читает файл с вакансиями json и сохраняет в список объектов Vacancy
        '''
        with (open(self.path, 'r', encoding='utf-8') as data_file):
            data = json.load(data_file)
            vacancies : list[Vacancy] = []
            for item in data:
                vacancy = Vacancy(item['name'], item['url'], item['salary_from'], item['salary_to'],
                                  item['salary'], item['currency'], item['experience'], item['date'])
                vacancies.append(vacancy)
            return vacancies

    def add_vacancy(self, vacancy):
        '''
        Функция добавляет одну вакансию в файл
        '''
        vacancies = self.read_data()
        vacancies.append(vacancy)
        self.save_data(vacancies)

    def get_vacancy(self, params):
        '''
        Функция принимает произвольное количество именованных переменных,
        имена должны совпадать со свойствами экземпляров вакансий,
        возвращает экземпляр найденной вакансии или список похожих вакансий
        '''
        if len(params) == 0:
            print('Параметры для поиска вакансии не заданы')
        else: # Если переданы именованные аргументы
            if params.get('name'):
                name = params['name']
            if params.get('salary_from'):
                salary_from = int(params['salary_from'])
            if params.get('salary_to'):
                salary_to = int(params['salary_to'])
            vacancies = self.read_data()
            founded_vacancies = []
            for vacancy in vacancies:
                if 'name' in locals() and vacancy.name.lower() == name.lower():
                    founded_vacancies.append(vacancy) # добавляем вакансию в список найденных
                    if 'salary_from' in locals() and vacancy._salary_from != salary_from:
                        founded_vacancies.remove(vacancy) # удаляем из списка
                    else:
                        if 'salary_to' in locals() and vacancy._salary_to == salary_to:
                            return founded_vacancies # Найдено точно совпадение вакансии по трем полям, отправляем пользователю
                        elif 'salary_to' not in locals() and vacancy._salary_to == None:
                            return founded_vacancies #
                        else:
                            founded_vacancies.remove(vacancy) # удаляем из списка
            return founded_vacancies

    def delete_vacancy(self, vacancy):
        '''
        Функция удаляет отобранную по критериям вакансию и сохраняет изменения в файл
        '''
        vacancies = self.read_data()
        vacancies.remove(vacancy)
        self.save_data(vacancies)

    @staticmethod
    def check_on_exist(file_name):
        '''
        Функция проверяет наличие файла по пути к файлу с данными,
        возвращает True в случае успеха
        '''
        path_data = os.path.join(ROOT_DIR, 'data', file_name)
        try:
            with open(path_data, mode='r', encoding='utf-8') as f:
                pass
            return True
        except FileNotFoundError:
            return False
