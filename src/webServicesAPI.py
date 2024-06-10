import requests
from abc import ABC, abstractmethod
from lxml import etree
from datetime import date, datetime


class Parser:

    @abstractmethod
    def load_data(self, keyword=None):
        pass


class HeadHunterAPI(Parser):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []

    def load_data(self, keyword=None):
        '''
        Функция отправляет запрос на платформу hh.ru,
        загружает данные и возращает в виде список словарей
        '''
        vacancies: list[dict] = []
        self.params['text'] = keyword
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            vacancies = response.json()['items']
        return vacancies


class CurrencyCourseAPI(Parser):
    '''
    Класс отправляет запрос на сайт Центрального Банка РФ,
    загружает файл в формате xml и парсит его
    '''
    courses = {}

    def __init__(self):
        current_date = datetime.now().date()
        formatted_date = current_date.strftime('%d/%m/%Y')
        self.url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req=' + formatted_date

    def load_data(self, keyword=None):
        '''
        Функция отправляет запрос, получает котировки валют,
        парсит данные и записывает курсы валют в атрибут класса course
        '''
        response = requests.get(self.url)
        names = ('KZT', 'BYR', 'USD', 'EUR')
        if response.status_code == 200:
            text_XML = response.content
            elements = etree.fromstring(text_XML, parser=etree.XMLParser(encoding='cp1251', recover=True))
            for currency in elements:
                for item in currency:
                    if item.text in names:
                        string_value = currency.find('Value').text
                        str_nominal = currency.find('Nominal').text
                        value = float(string_value.replace(',', '.')) / float(str_nominal.replace(',', '.'))
                        value = round(value, 2)
                        self.courses[item.text] = value

