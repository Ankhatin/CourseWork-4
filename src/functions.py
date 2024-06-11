import re


def filter_vacancies(vacancies, filter_words):
    '''
    Функция принимает ключевые слова для фильтрации вакансий,
    если хоть одно из слов встречается в наименовании вакансии
    вакансия добавляется в список для передачи в вызывающую функцию
    '''
    filtered_vacancies = []
    filter_set = []
    for word in filter_words: # формируем множество ключевых слов с учетом регистра
        filter_set.append(word.lower()) # слово в нижнем регистре
    filter_set = set(filter_set) # создаем множество, устраняем дублирующие слова
    for vacancy in vacancies:
        vacancy_set = []
        vacancy_words = vacancy.name.split()
        for word in vacancy_words: # то же самое со списком слов из наименования вакансии
            vacancy_set.append(word.lower())
        vacancy_set = set(vacancy_set)
        if vacancy_set.intersection(filter_set): # Если хоть одно из слов в множествах совпали записываем вакансию в список
            filtered_vacancies.append(vacancy)
    return filtered_vacancies

def filter_by_experience(vacancies, filter):
    '''
    Функция фильтрует список вакансий по значению свойства "Опыт"
    '''
    filtered_vacancies = []
    filter = filter.lower()
    for vacancy in vacancies:
        if filter.lower() in vacancy.experience: # если хоть одно из слов в множествах совпали записываем вакансию в список
            filtered_vacancies.append(vacancy)
    return filtered_vacancies

def filter_by_salary(vacancies, filter):
    '''
    Функция принимает список вакансий, фильтр из двух чисел
    и фильтрует вакансии по значениям зарплат
    '''
    filtered_vacancies = []
    for vacancy in vacancies:
        if vacancy.salary == 'Зарплата не указана':
            continue
        # Проверяем вариант, когда пользователь указал только поле "Зарплата от"
        if len(filter) == 1:
            if vacancy._salary_from and vacancy.salary_from >= filter[0]: # Если есть поле "Зарплата от" в вакансии проверяем больше ли оно нижней границы диапозона
                filtered_vacancies.append(vacancy)
            elif not vacancy._salary_from and vacancy.salary_to >= filter[0]:
                filtered_vacancies.append(vacancy)
        else: # Если пользователь указал поля "Зарплата от" и "Зарплата до"
            if vacancy._salary_from and vacancy._salary_to:
                if vacancy.salary_from >= filter[0] and vacancy.salary_to >= filter[1]:
                    filtered_vacancies.append(vacancy)
            elif vacancy._salary_from and vacancy.salary_from >= filter[0]:
                filtered_vacancies.append(vacancy)
            elif vacancy._salary_to and vacancy.salary_to >= filter[1]:
                filtered_vacancies.append(vacancy)
    return filtered_vacancies


def sort_vacancies(vacancies):
    '''
    Функция принимает список вакансий и сортирует их по значению зарплат
    '''
    vacancies.sort(key=sort_key, reverse=True)
    return vacancies


def sort_key(vacancy):
    '''
    Функция-ключ для сортировки вакансий по значению зарплат
    '''
    return vacancy


def get_salary_range(filter):
    '''
    Функция принимает строку из двух чисел, введенных пользователем
     и проверяет являются ли переданные данные числами и первое значение меньше второго
    '''
    filter_list = [] # список со значениями диапазона зарплат
    pattern = re.compile(r'\d+\D*\d*')
    if pattern.search(filter): # Если соответствие найдено по индексу находим искомую строку со значениями диапазона
        filter = pattern.search(filter)[0]
    filter = re.split(r'\D+', filter)
    for item in filter:
        filter_list.append(int(item))
    if len(filter_list) == 2 and (filter_list[0] < filter_list[1]):
        return filter_list
    return filter_list


def print_top(vacancies, number):
    '''
    Функция принимает список вакансий и выводит на экран
    в количестве, равном аргументу number
    '''
    for n in range(number):
        print(vacancies[n])


