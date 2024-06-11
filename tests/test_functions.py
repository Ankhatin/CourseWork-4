from src.functions import *
from src.vacancies import *
from src.webServicesAPI import *
from src.file_manager import *
from main import user_interaction
import pytest

test_dict = [{'id': '101532598', 'premium': False, 'name': 'Python разработчик (Django)', 'department': None, 'has_test': False, 'response_letter_required': False, 'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'}, 'salary': {'from': 500, 'to': 980, 'currency': 'USD', 'gross': False}, 'type': {'id': 'open', 'name': 'Открытая'}, 'address': None, 'response_url': None, 'sort_point_distance': None, 'published_at': '2024-06-05T23:46:41+0300', 'created_at': '2024-06-07T23:46:41+0300', 'archived': False, 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=101532598', 'show_logo_in_search': None, 'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/101532598?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/101335947', 'relations': [], 'employer': {'id': '11131363', 'name': 'Gybernaty', 'url': 'https://api.hh.ru/employers/11131363', 'alternate_url': 'https://hh.ru/employer/11131363', 'logo_urls': {'90': 'https://img.hhcdn.ru/employer-logo/6766930.png', 'original': 'https://img.hhcdn.ru/employer-logo-original/1286658.png', '240': 'https://img.hhcdn.ru/employer-logo/6766931.png'}, 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=11131363', 'accredited_it_employer': False, 'trusted': False}, 'snippet': {'requirement': 'Отличные знания одного из языков программирования: TypeScript, <highlighttext>Python</highlighttext>, Go, Rust, Dart. Опыт работы с фреймворками и технологиями. Опыт работы с...', 'responsibility': 'Разработка и поддержка передовых проектов. Постоянное обучение и освоение новых технологий. Работа в команде, обмен опытом и знаниями. '}, 'contacts': None, 'schedule': {'id': 'remote', 'name': 'Удаленная работа'}, 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': False, 'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}], 'accept_incomplete_resumes': True, 'experience': {'id': 'between1And3', 'name': 'От 1 года до 3 лет'}, 'employment': {'id': 'probation', 'name': 'Стажировка'}, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}]

test_list_vacancies = [{"name": "Python разработчик (Django)","url": "https://hh.ru/vacancy/101335947",
                        "salary_from": 500, "salary_to": 980,
                        "salary": "Зарплата от 500 до 980 USD", "currency": "USD",
                        "experience": "от 1 до 3 лет", "date": "05.06.2024"},
                       {"name": "Python разработчик (Intern)", "url": "https://hh.ru/vacancy/101350542",
                        "salary_from": 600, "salary_to": None,
                        "salary": "Зарплата от 600 USD", "currency": "USD",
                        "experience": "без опыта", "date": "05.06.2024"},
                       {"name": "Python разработчик", "url": "https://hh.ru/vacancy/101350542",
                        "salary_from": 50000, "salary_to": 80000,
                        "salary": "Зарплата от 50000 до 80000 руб.", "currency": "руб.",
                        "experience": "без опыта", "date": "05.06.2024"},
                        {"name": "C++ разработчик", "url": "https://hh.ru/vacancy/101350542",
                        "salary_from": 60000, "salary_to": 100000,
                        "salary": "Зарплата от 60000 до 100000 руб.", "currency": "руб.",
                        "experience": "от 1 до 3 лет", "date": "05.06.2024"}
                       ]
test_list_vacancies_with_equal = [{"name": "Python разработчик (Django)",
                        "url": "https://hh.ru/vacancy/101335947",
                        "salary_from": 500, "salary_to": 980,
                        "salary": "Зарплата от 500 до 980 USD", "currency": "USD",
                        "experience": "от 1 до 3 лет", "date": "05.06.2024"},
                       {"name": "Python разработчик (Django)",
                        "url": "https://hh.ru/vacancy/101335947",
                        "salary_from": 500, "salary_to": 980,
                        "salary": "Зарплата от 500 до 980 USD", "currency": "USD",
                        "experience": "от 1 до 3 лет", "date": "05.06.2024"}]

file_json = FileManager('vacancies.json')
currencies = CurrencyCourseAPI()
currencies.load_data()
vacancy_instance = Vacancy(name='Python разработчик (Django)', url='https://hh.ru/vacancy/101335947',
                  salary_from=500, salary_to=980, salary="Зарплата от 500 до 980 USD", currency="USD",
                  experience="от 1 до 3 лет", date = "05.06.2024")




def build_list_vacancies(lst):
    '''
    Функция формирует список экземпляов вакансий для
    сравнения выходных данных тестируемых функций
    '''
    vacancies = []
    for item in lst:
        vacancy = Vacancy(item['name'], item['url'], item['salary_from'], item['salary_to'],
                          item['salary'], item['currency'], item['experience'], item['date'])
        vacancies.append(vacancy)
    return vacancies

def test_load_vacancies():
    object_API = HeadHunterAPI()
    assert len(object_API.load_data()) == 100
    object_API.url = 'https://api.hh.ru/vacancies&&'
    assert len(object_API.load_data()) == 0


def test__eq__():
    '''
    Функция проверяет экземпляры вакансий на равенство
    '''
    vacancies = build_list_vacancies(test_list_vacancies_with_equal)
    assert vacancies[0] == vacancies[1]

def test__lt__():
    '''
    Функция проверяет экземпляры вакансий на больше и меньше
    '''
    vacancies = build_list_vacancies(test_list_vacancies)
    assert vacancies[0] < vacancies[1]


def test_salary_from():
    salary_from = 500 * CurrencyCourseAPI.courses['USD']
    assert vacancy_instance.salary_from == salary_from


def test_salary_to():
    salary_to = 980 * CurrencyCourseAPI.courses['USD']
    assert vacancy_instance.salary_to == salary_to


def test_build_object_list():
    assert Vacancy.build_object_list(test_dict)[0] == vacancy_instance


def test_format_instance_to_dict():
    assert vacancy_instance.format_instance_to_dict() == {"name": "Python разработчик (Django)",
                                                          "url": "https://hh.ru/vacancy/101335947",
                                                          "salary_from": 500, "salary_to": 980,
                                                          "salary": "Зарплата от 500 до 980 USD", "currency": "USD",
                                                          "experience": "от 1 до 3 лет", "date": "05.06.2024"}

def test_build_salary():
    assert Vacancy.build_salary(60000, 100000, 'руб.') == 'Зарплата от 60000 до 100000 руб.'


def test_read_data():
    vacancies = build_list_vacancies(test_list_vacancies)
    file_json.save_data(vacancies)
    assert file_json.read_data() == vacancies


def test_get_vacancy():
    '''
    Функция тестирует get_vacancy()
    ищем вакансию по переданным параметрам в списке из двух вакансий
    '''
    vacancies = build_list_vacancies(test_list_vacancies)
    params = {'name': 'Python разработчик (Django)', 'salary_from': 500, 'salary_to': 980}
    # Тестируем функцию, передав ей три аргумента
    assert file_json.get_vacancy(params)[0] == vacancy_instance
    params = {'name': 'Python разработчик (Intern)', 'salary_from': 600}
    # Тестируем функцию, передав два аргумента, при условии что свойство "Зарплата от" у найденной вакансии также отсутствует
    assert file_json.get_vacancy(params)[0] == vacancies[1]


def test_check_on_exist():
    assert file_json.check_on_exist('data.json') == False


def test_filter_vacancies():
    '''
    Функция тестирует функцию фильтрации вакансий по ключевым словам в наименовании
    '''
    vacancies = build_list_vacancies(test_list_vacancies)
    filter_words = 'C++'.split()
    assert filter_vacancies(vacancies, filter_words)[0] == Vacancy(name="C++ разработчик", url="https://hh.ru/vacancy/101350542",
                                                                salary_from=60000, salary_to=100000,
                                                                salary="Зарплата от 60000 до 100000 руб.", currency="руб.",
                                                                experience="от 1 до 3 лет", date="05.06.2024")
    with pytest.raises(IndexError): # Проверяем, есть ли еще вакансии в списке
        assert filter_vacancies(vacancies, filter_words)[1]


def test_filter_by_experience():
    '''
    Функция сортирует список экземпляров вакансий по свойству "experience"
    '''
    vacancies = build_list_vacancies(test_list_vacancies)
    experience = 'от 1 до 3 лет'
    assert filter_by_experience(vacancies, experience) == [Vacancy(name="Python разработчик (Django)",
                                                            url="https://hh.ru/vacancy/101335947",
                                                            salary_from=500, salary_to=980,
                                                            salary="Зарплата от 500 до 980 USD", currency="USD",
                                                            experience="от 1 до 3 лет", date="05.06.2024"),
                                                            Vacancy(name="C++ разработчик",
                                                            url="https://hh.ru/vacancy/101350542",
                                                            salary_from=60000, salary_to=100000,
                                                            salary="Зарплата от 60000 до 100000 руб.", currency="руб.",
                                                            experience="от 1 до 3 лет", date="05.06.2024")]

def test_filter_by_salary():
    '''
    Функция сортирует список экземпляров вакансий по свойству "experience"
    '''
    vacancies = build_list_vacancies(test_list_vacancies)
    salary_range = [60000, 80000]
    assert filter_by_salary(vacancies, salary_range) == [Vacancy(name="C++ разработчик",
                                                                url="https://hh.ru/vacancy/101350542",
                                                                salary_from=60000, salary_to=100000,
                                                                salary="Зарплата от 60000 до 100000 руб.", currency="руб.",
                                                                experience="от 1 до 3 лет", date="05.06.2024")]
    salary_range = [60000]
    assert filter_by_salary(vacancies, salary_range) == [Vacancy(name="C++ разработчик",
                                                                 url="https://hh.ru/vacancy/101350542",
                                                                 salary_from=60000, salary_to=100000,
                                                                 salary="Зарплата от 60000 до 100000 руб.",
                                                                 currency="руб.",
                                                                 experience="от 1 до 3 лет", date="05.06.2024")]


def test_sort_vacancies():
    '''
    Функция сортирует список экземпляров вакансий по зарплате
    '''
    input_list = build_list_vacancies(test_list_vacancies)
    # Инициализируем список вакансий в нужном порядке для сравнения с выходными даными
    output_vacancies = [{"name": "C++ разработчик","url": "https://hh.ru/vacancy/101350542",
                        "salary_from": 60000, "salary_to": 100000,
                        "salary": "Зарплата от 60000 до 100000 руб.", "currency": "руб.",
                        "experience": "от 1 до 3 лет", "date": "05.06.2024"},
                        {"name": "Python разработчик (Intern)", "url": "https://hh.ru/vacancy/101350542",
                         "salary_from": 600, "salary_to": None,
                         "salary": "Зарплата от 600", "currency": "USD",
                         "experience": "без опыта", "date": "05.06.2024"},
                        {"name": "Python разработчик", "url": "https://hh.ru/vacancy/101350542",
                         "salary_from": 50000, "salary_to": 80000,
                         "salary": "Зарплата от 50000 до 80000 руб.", "currency": "руб.",
                         "experience": "без опыта", "date": "05.06.2024"},
                        {"name": "Python разработчик (Django)", "url": "https://hh.ru/vacancy/101335947",
                        "salary_from": 500, "salary_to": 980,
                        "salary": "Зарплата от 500 до 980 USD", "currency": "USD",
                        "experience": "от 1 до 3 лет", "date": "05.06.2024"}
                        ]
    output_list = build_list_vacancies(output_vacancies)
    assert sort_vacancies(input_list) == output_list


def test_get_salary_range():
    filter = 'от 50000'
    assert get_salary_range(filter) == [50000]
    filter = '50000 --  80000'
    assert get_salary_range(filter) == [50000, 80000]

