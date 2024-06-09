import re
def filter_vacancies(vacancies, filter_words):
    '''
    Функция принимает ключевые слова для фильтрации вакансий,
    если хоть одно из слов встречается в наименовании вакансии
    она попадает в список, который возрващается в вызывающую функцию
    '''
    filtered_vacancies = []
    filter_set = []
    for word in filter_words: # формируем множество ключевых слов
        filter_set.append(word)
        filter_set.append(word.lower()) # слово в нижнем регистре
        filter_set.append(word.title()) # слово с первой заглавной буквы
    filter_set = set(filter_set) # создаем множество, устраняем дублирующие слова
    for vacancy in vacancies:
        vacancy_set = []
        vacancy_words = vacancy.name.split()
        for word in vacancy_words: # то же самое со списком слов из наименования вакансии
            vacancy_set.append(word)
            vacancy_set.append(word.lower())
            vacancy_set.append(word.title())
        vacancy_set = set(vacancy_set)
        if vacancy_set.intersection(filter_set):# если хоть одно из слов в множествах совпали записываем вакансию в список
            filtered_vacancies.append(vacancy)
    return filtered_vacancies

def filter_by_experience(vacancies, filter):
    filtered_vacancies = []
    filter = filter.lower()
    for vacancy in vacancies:
        if filter in vacancy.experience.lower(): # если хоть одно из слов в множествах совпали записываем вакансию в список
            filtered_vacancies.append(vacancy)
    return filtered_vacancies

def filter_by_salary(vacancies, filter):
    filtered_vacancies = []
    filter_list = re.split(r'\D+', filter)
    for vacancy in vacancies:
        if vacancy.salary == 'Зарплата не указана':
            continue
        if vacancy.salary_from:
            if int(filter_list[0]) <= vacancy.salary_from:
                filtered_vacancies.append(vacancy)
        elif vacancy.salary_to:
            if vacancy.salary_to > int(filter_list[0]):
                filtered_vacancies.append(vacancy)

def sort_vacancies(vacancies):
    vacancies.sort(key=sort_list, reverse=True)
    return vacancies

def sort_list(vacancy):
    return vacancy

def check_salary_on_correct(filter):
    filter_list = re.split(r'\D+', filter)
    if filter_list[0].isdigit() and filter_list[1].isdigit():
        return int(filter_list[0]) < int(filter_list[1])




