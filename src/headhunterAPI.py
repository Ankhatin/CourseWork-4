import requests
from abc import ABC, abstractmethod


class Parser:

    @abstractmethod
    def load_vacancies(self, keyword):
        pass


class HeadHunterAPI(Parser):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []

    def load_vacancies(self, keyword):
        self.params['text'] = keyword
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
        return self.vacancies
