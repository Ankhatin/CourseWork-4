import datetime
from src.webServicesAPI import CurrencyCourseAPI

class Vacancy:
    name: str
    url: str
    salary: str
    _salary_from: int
    _salary_to: int
    experience: str
    currency: str
    date: datetime

    def __init__(self, name, url, salary_from, salary_to, salary, currency, experience, date):
        self.name = name
        self.url = url
        self._salary_from = salary_from
        self._salary_to = salary_to
        self.salary = salary
        self.currency = currency
        self.experience = experience
        self.date = date

    def __eq__(self, other):
        '''
        Метод переопределяет операцию сравнения "==" для сравнения объектов вакансий,
        в качестве критерия для сравнения используются свойства "Зарплата от" и "Зарплата до"
        '''
        if self.salary == 'Зарплата не указана' and other.salary == 'Зарплата не указана':
            return True
        elif self.salary_from and other.salary_from\
                and self.salary_to and other.salary_to: # Если оба свойства зарплат вакансий заданы
            return self.salary_from == other.salary_from\
                and self.salary_to == other.salary_to
        elif self.salary_from and other.salary_from\
                and not self.salary_to and not other.salary_to: # Если заданы только свойства "Зарплата от"
            return self.salary_from == other.salary_from
        elif not self.salary_from and not other.salary_from\
                and self.salary_to and other.salary_to: # Если заданы только свойства "Зарплата до"
            return self.salary_to == other.salary_to

    def __lt__(self, other):
        '''
        Метод переопределяет операцию сравнения "<" и ">" для сравнения объектов вакансий,
        в качестве критерия для сравнения используются свойства "Зарплата от" и "Зарплата до",
        свойство "Зарплата от" имеет приоритетное значение
        '''
        if self.salary_from and other.salary_from: # Если указаны свойства "Зарплата от" то сравниваем по ним
            return self.salary_from < other.salary_from
        elif self.salary_from: # Если задана "Зарплата от" только у первой вакансии, значит она больше
            return False
        elif other.salary_from: # Если задана только у второй, то первая вакансия меньше
            return True
        elif self.salary_to and other.salary_to: # Если заданы только свойства "Зарплата до"
            return self.salary_to < other.salary_to
        elif other.salary_to: # Если у первого объекта зарплата не указана, а у второго указана "Зарплата до"
            return other.salary_to
        elif self.salary_to: # и наоборот
            return False

    def __str__(self):
        return f'{self.name}, {self.url}, {self.salary}, {self.experience}'


    @property
    def salary_from(self):
        '''
        Создаем декоратор для свойства "Зарплата от" который в случае
        если сумма указана в валюте будет возвращать значение е рублях
        '''
        if self.currency in ('KZT', 'USD', 'EUR'):
            if self._salary_from:
                return self._salary_from * CurrencyCourseAPI.courses[self.currency]
            else:
                return self._salary_from
        else:
            return self._salary_from

    @property
    def salary_to(self):
        '''
        Создаем декоратор для свойства "Зарплата до" который в случае
        если сумма указана в валюте будет возвращать значение е рублях
        '''
        if self.currency in ('KZT', 'USD', 'EUR'):
            if self._salary_to:
                return self._salary_to * CurrencyCourseAPI.courses[self.currency]
            else:
                return self._salary_to
        else:
            return self._salary_to

    @classmethod
    def build_object_list(cls, vacancies):
        vacancies_list = []
        for vacancy in vacancies:
            url = ''
            salary_from = None
            salary_to = None
            salary = ''
            currency = ''
            experience = ''
            date = ''
            # проверяем наличие в вакансии значимых полей с данными
            name = vacancy['name']
            if vacancy.get('alternate_url'):
                url = vacancy.get('alternate_url')
            else:
                url = 'Ссылка отсутствует'
            if vacancy.get('salary'):
                salary_from = vacancy['salary']['from']
                salary_to = vacancy['salary']['to']
                if vacancy['salary']['currency'] == 'RUR':
                    currency = 'руб.'
                elif vacancy['salary']['currency'] == 'KZT':
                    currency = 'KZT'
                elif vacancy['salary']['currency'] == 'USD':
                    currency = 'USD'
                elif vacancy['salary']['currency'] == 'EUR':
                    currency = 'EUR'
                salary = cls.build_salary(salary_from, salary_to, currency)
            else:
                salary = "Зарплата не указана"
            if vacancy.get('experience'):
                if vacancy['experience']['id'] == 'noExperience':
                    experience = 'Без опыта'
                elif vacancy['experience']['id'] == 'between1And3':
                    experience = 'От 1 до 3 лет'
                elif vacancy['experience']['id'] == 'between3And6':
                    experience = 'От 3 до 6 лет'
                else:
                    experience = 'Нет данных'
            # Конвертируем дату из формата ISO строки в объект datetime и отсекаем время
            if vacancy.get('date'):
                date = datetime.datetime.fromisoformat(vacancy['date']).date()
                date = date.strftime("%d.%m.%Y")
            vacancy_instance = cls(name, url, salary_from, salary_to, salary, currency, experience, date)
            vacancies_list.append(vacancy_instance)
        return vacancies_list

    def format_instance_to_dict(self):
        instance_in_dict = dict(name=self.name, url=self.url, salary_from=self._salary_from, salary_to=self._salary_to,
                                salary=self.salary, currency=self.currency, experience=self.experience, date=self.date)
        return instance_in_dict

    @staticmethod
    def build_salary(salary_from, salary_to, currency):
        '''
        Функция формирует строку для отображения в удобном формате
        '''
        if not salary_from:
            salary = f'Зарплата до {salary_to} {currency}'
        else:
            salary = f'Зарплата от {salary_from} {currency}'
        return salary

