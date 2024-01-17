from src.vacancies_API import HeadHunterAPI
from src.functions import print_employers, get_data, create_database, save_data_to_database
from src.config import config
from src.DBManager import DBManager, DATABASE_NAME


def main():
    """Функция для взаимодействия с пользователем"""
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()

    # Получение работодателей

    counter = 3
    hh_employers = {'items': []}
    while counter > 0 and hh_employers['items'] == []:
        city = input('Введите регион поиска вакансий(город): ').lower()
        # пермь
        hh_employers = hh_api.get_employers(city)
        # print(hh_employers)
        if hh_employers['items']:
            print_employers(hh_employers)
        else:
            print("Вакансий в заданном городе не найдено. Попробуйте ещё")
        counter -= 1

    if counter != 0 or hh_employers['items'] != []:
        # Получение вакансий по id работодателей
        employers_id_list = []
        while employers_id_list == []:
            employers_id_list = input('Введите id работодателей из списка через запятую: ')
            # 9430380, 3591994, 927820, 3192921, 4069218, 550628, 10138825, 9200839, 3085702, 2146655
            # 9430380, !3591994, , , сврср5468паао, 927820,, 3192921,
            employers_id_list = employers_id_list.split(',')
            employers_id_list = [int(i.strip()) for i in employers_id_list if i.strip().isdigit()]
            hh_vacancies = []
            if employers_id_list:
                hh_vacancies = hh_api.get_vacancies(employers_id_list)
                if not hh_vacancies['items']:
                    print(f'Вакансии с id = {employers_id_list} не найдены')
            else:
                print('Ошибка ввода.')

        # Получение списка словарей с работодателями и их вакансиями
        data = get_data(hh_employers, hh_vacancies, employers_id_list)
        for dictionary in data:
            print(dictionary)

        # Получение параметров подключения к БД
        params = config()

        # Создание БД
        create_database(DATABASE_NAME, params)

        # Сохранение данных в БД
        save_data_to_database(DATABASE_NAME, data, params)

        # Работа с БД
        db = DBManager()

        result = db.get_companies_and_vacancies_count()
        if result:
            print('Список всех компаний и количество вакансий')
            for employer in result:
                print(employer)
        else:
            print("Нет компаний, соответствующих заданным критериям")

        result = db.get_all_vacancies()
        if result:
            print('Список всех вакансий')
            for i, vacancy in enumerate(result, 1):
                print(i, vacancy)
        else:
            print('Нет вакансий, соответствующих заданным критериям')

        result = db.get_avg_salary()
        if result:
            print('Средняя зарплата по вакансиям')
            print(result)
        else:
            print('Средняя зарплата не найдена')

        result = db.get_vacancies_with_higher_salary()
        if result:
            print('Список вакансий, зарплата которых выше средней')
            for i, vacancy in enumerate(result, 1):
                print(i, vacancy)
        else:
            print('Нет вакансий, соответствующих заданным критериям')

        keyword = input("Введите ключевое слово для фильтрации вакансий: ")
        result = db.get_vacancies_with_keyword(keyword)
        if result:
            print(f'Список вакансий по запросу {keyword}')
            for i, vacancy in enumerate(result, 1):
                print(i, vacancy)
        else:
            print('Нет вакансий, соответствующих заданным критериям')

    else:
        print("Вакансии не найдены.\nЗавершение работы программы ...")


if __name__ == "__main__":
    main()
