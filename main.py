import os.path

from src.webServicesAPI import HeadHunterAPI, CurrencyCourseAPI
from src.file_manager import *
from src.vacancies import *
from src.functions import *
import os.path

ROOT_DIR = os.path.dirname(__file__)


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
        search_query = input("Введите поисковый запрос для отбора вакансий на сайтах платформы hh.ru.\n"
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

    # Фильтруем вакансии по полю "опыт"
    experience = input('Введите опыт работы или Enter, чтобы пропустить: ').lower()
    if experience:
        filtered_by_experience = filter_by_experience(filtered_data, experience)
    else:
        filtered_by_experience = filtered_data
    print(f'Получено {len(filtered_by_experience)} вакансий')

    # Фильтруем вакансии по диапазону зарплат
    salary_range = input('Введите диапазон зарплат или Enter, чтобы пропустить: ')
    if salary_range: # Если не пустой диапазон зарплат
        filter_salary = get_salary_range(salary_range) # Формируем из строки список за значениям зарплат
        if filter_salary:
            filtered_by_salary = filter_by_salary(filtered_by_experience, filter_salary)
        else:
            print ('Введен некорректный диапазон зарплат')
            filtered_by_salary = filtered_by_experience
    else:
        filtered_by_salary = filtered_by_experience
    print(f'Получено {len(filtered_by_salary)} вакансий')

    # Сортируем вакансии по зарплате
    if input('Сортировать вакансии по зарплате, Да или Enter, чтобы пропустить: ').lower() == 'да':
        sorted_vacancies = sort_vacancies(filtered_by_salary)
    else:
        sorted_vacancies = filtered_by_salary  # если не задано оставляем список без изменений
    top_n = input('Введите количество вакансий для вывода на экран или Enter, чтобы вывести все: ')
    if top_n.isdigit():
        print_top(sorted_vacancies, int(top_n))
    elif top_n == '':
        print_top(sorted_vacancies, len(sorted_vacancies))
    else:
        print("Введено некорретное значение")
    if input('Сохранить список вакансий в файл (да/нет): ').lower() == 'да':
        file_json.save_data(sorted_vacancies)

    # Добавляем произвольную вакансию в файл
    new_vacancy = Vacancy('Python разработчик', '', 50000, 100000,
                          'Зарплата от 50000 до 100000 руб.', 'руб.', 'Без опыта', '')
    file_json.add_vacancy(new_vacancy)

    if input('Осуществить поиск вакансий, "да" или Enter, чтобы пропустить: ').lower() == 'да':
        # Формируем список значений для поиска, упаковываем в словарь для передачи в функцию
        keylist, valuelist = [], []
        name = input('Введите нименование вакансии: ')
        keylist.append('name')
        valuelist.append(name)
        salary_from = input('Введите значение "Зарплата от" или Enter, чтобы пропустить: ').strip()
        if salary_from != '' and salary_from.isdigit():
            keylist.append('salary_from')
            valuelist.append(salary_from)
        salary_to = input('Введите значение "Зарплата до" или Enter, чтобы пропустить: ').strip()
        if salary_to != '' and salary_to.isdigit():
            keylist.append('salary_to')
            valuelist.append(salary_to)
        params = dict(zip(keylist, valuelist)) # Список параметров для поиска упаковываем в словарь
        founded_vacancies = file_json.get_vacancy(params)
        if len(founded_vacancies) > 0: # если найдены вакансии
            if input(f'Найдено вакансий {len(founded_vacancies)}, \'да\', чтобы вывести на экран, Enter пропустить').lower():
                print_top(founded_vacancies, len(founded_vacancies))
        else:
            print('Не найдено ни одного совпадения')
        if len(founded_vacancies) == 1: # если в списке найденных только одна вакансия
            if input(f'Удалить найденную вакансию, \'да\', или Enter, чтобы пропустить').lower() == 'да':
                file_json.delete_vacancy(founded_vacancies[0])
        if input('Сформировать новый запрос, "да" или Enter, чтобы пропустить: ').lower() == 'да':
            user_interaction()

if __name__ == '__main__':
    # Инициализируем объект для работы с API hh.ru
    hh_api = HeadHunterAPI()
    # Инициализируем объект для работы с API Центрального Банка РФ
    currencies = CurrencyCourseAPI()
    currencies.load_data() # загружаем курсы нужных нам валют и сохраняем в атрибут класса в виде словаря
    user_interaction()

