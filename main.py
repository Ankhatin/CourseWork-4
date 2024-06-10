from src.webServicesAPI import HeadHunterAPI, CurrencyCourseAPI
from src.file_manager import *
from src.vacancies import *
from src.functions import *


# Функция для взаимодействия с пользователем
def user_interaction():
    '''
    Функция реализует взаимодействие с пользователем
    '''
    vacancies: list[Vacancy] = []
    file_json = FileManager('vacancies.json')
    # Если существует файл с данными предлагаем пользователю загрузить вакансии из него
    if FileManager.check_on_exist('vacancies.json') and \
            input('Загрузить ранее сохраненные вакансии из файла (да/нет): ').lower() == 'да':
        vacancies = file_json.read_data()
    else:
        search_query = input("Введите поисковый запрос для поиска вакансий на сайтах платформы hh.ru."
                             "Названия профессий, специальностей, умения, навыки: ")
        hh_vacancies = hh_api.load_data(search_query)
        vacancies = Vacancy.build_object_list(hh_vacancies)
        file_json.save_data(vacancies)

    print('''Введите ключевые слова для отбора вакансий. 
    Возможные критерии для поиска:
    1. Ключевые слова в наименовании вакансии, например 'Разработчик'
    2. Опыт работы. Возможные варианты: 'Без опыта', 'От 1 до 3 лет', 'От 3 до 6 лет' 
    2. Диапазон зарплат, два числа. Возможные варианты: 50000 - 100000, 40000  80000 и т.д.''')
    keywords = input('Введите ключевые слова для более строгого отбора в наименовании вакансии '
                     'или Enter, чтобы пропустить: ').split()
    if keywords:
        filtered_data = filter_vacancies(vacancies, keywords)
    else:
        filtered_data = vacancies # Если не задано оставляем список без изменений
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
            filtered_by_salary = filter_by_salary(filtered_by_experience, salary_range)
        else:
            print ('Введен некорректный диапазон зарплат')
            filtered_by_salary = filtered_by_experience
    else:
        filtered_by_salary = filtered_by_experience
    print(f'Получено {len(filtered_by_salary)} вакансий')
    if input('Сортировать вакансии по зарплате, Да или Enter, чтобы пропустить: ').lower() == 'да':
        sorted_vacancies = sort_vacancies(filtered_by_salary)
    else:
        sorted_vacancies = filtered_by_salary  # если не задано оставляем список без изменений
    top_n = input('Введите количество вакансий для вывода на экран или Enter, чтобы вывести все: ')
    if top_n.isdigit():
        print_top(sorted_vacancies, int(top_n))
    else:
        print("Введено некорретное значение")
        print_top(sorted_vacancies, len(sorted_vacancies))
    if input('Сохранить список вакансий в файл (да/нет): ').lower() == 'да':
        file_json.save_data(sorted_vacancies)
    #
    new_vacancy = Vacancy('Python разработчик', '', 50000, 100000,
                          'Зарплата от 50000 до 100000 руб.', 'руб.', 'Без опыта', '')
    file_json.add_vacancy(new_vacancy)
    vacancy = file_json.get_vacancy(name="Python разработчик", salary_from=50000, salary_to=100000)
    if vacancy:
        file_json.delete_vacancy(vacancy)


if __name__ == '__main__':
    # Инициализируем объект для работы с API и файловый менеджер
    hh_api = HeadHunterAPI()
    currencies = CurrencyCourseAPI()
    currencies.load_data() # загружаем курсы нужных нам валют и сохраняем в атрибут класса
    user_interaction()

