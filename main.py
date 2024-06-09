from src.webServicesAPI import HeadHunterAPI, CurrencyCourseAPI
from src.file_manager import *
from src.vacancies import *
from src.functions import *


# Функция для взаимодействия с пользователем
def user_interaction():
    #search_query = input("Введите поисковый запрос: ")
    hh_vacancies = hh_api.load_data('Python')
    vacancies = Vacancy.build_object_list(hh_vacancies)
    file_json.save_data(vacancies)
    #vacancies = []
    #vacancies_json = file_json.read_data()
    #for vacancy in vacancies_json:
    #    vacancies.append(Vacancy(vacancy['name'], vacancy['url'], vacancy['salary_from'], vacancy['salary_to'],
    #                             vacancy['salary'], vacancy['currency'], vacancy['experience'], vacancy['date']))
    filtered_data = []
    print('''Введите ключевые слова для отбора вакансий. 
    Возможные критерии для поиска:
    1. Слова в наименовании вакансии, например 'Разработчик'
    2. Опыт работы. Возможные варианты: 'Без опыта', 'От 1 до 3 лет', 'От 3 до 6 лет' 
    2. Диапазон зарплат. Возможные варианты: 50000 - 100000, 50000 100000''')
    keywords = input('Введите ключевые слова для поиска в наименовании вакансии или Enter, чтобы пропустить: ').split()
    if keywords:
        filtered_data = filter_vacancies(vacancies, keywords)
    else:
        filtered_data = vacancies # если не задано оставляем список без изменений
    print(f'Получено {len(filtered_data)} вакансий')
    experience = input('Введите опыт работы или Enter, чтобы пропустить: ')
    if experience:
        filtered_by_experience = filter_by_experience(filtered_data, experience)
    else:
        filtered_by_experience = filtered_data
    print(f'Получено {len(filtered_by_experience)} вакансий')
    salary_range = input('Введите диапазон зарплат или Enter, чтобы пропустить: ')
    if salary_range:
        if check_salary_on_correct(salary_range):
            filtered_by_salary = filter_by_salary(vacancies, salary_range)
        else:
            print ('Ввели некорректный диапазон зарплат')
            user_interaction()
    else:
        filtered_by_salary = filtered_by_experience
    print(f'Получено {len(filtered_by_salary)} вакансий')
    sort_it = input('Сортировать вакансии по зарплате, если Да, то любой символ, или Enter, чтобы пропустить: ')
    if sort_it:
        sorted_vacancies = sort_vacancies(vacancies)
    else:
        sorted_vacancies = filtered_by_salary  # если не задано оставляем список без изменений

    top_n = input('Введите количество вакансий для вывода на экран: ')
    if top_n.isdigit():
        print_top(int(top_n))
    else:
        print("Введено некорретное значение")


    new_vacancy = Vacancy('Python разработчик', '', 50000, 100000,
                          'Зарплата от 50000 до 100000 руб.', 'руб.', 'Без опыта', '')
    file_json.add_vacancy(new_vacancy)


if __name__ == '__main__':
    # Инициализируем объект для работы с API и файловый менеджер
    hh_api = HeadHunterAPI()
    file_json = FileManager('vacancies.json')
    currencies = CurrencyCourseAPI()
    currencies.load_data() # загружаем курсы нужных нам валют и сохраняем в атрибут класса
    user_interaction()

