from typing import Any
from datetime import date
# import psycopg2


# def filter_vacancies(hh_vacancies, filter_words):
#     """Функция, фильтрующая вакансии с сайтов hh и superjob"""
#     new_list = []
#     filter_words = set(filter_words)
#     punc = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
#
#     if os.path.exists('filtered.json'):
#         with open('filtered.json', 'w', encoding='utf-8') as f:
#             json.dump(new_list, f, ensure_ascii=False)
#
#     with open(hh_vacancies, 'r', encoding='utf-8') as f:
#         content = json.load(f)
#
#     # Цикл по вакансиям hh
#     for vacancy in content:
#
#         requirements = vacancy['requirements']
#         if requirements is None:
#             requirements = set()
#         else:
#             for s in requirements:
#                 if s in punc:
#                     new_str = requirements.replace(s, "")
#             requirements = set(new_str.lower().split())
#
#         description = vacancy['description']
#         if description is None:
#             description = set()
#         else:
#             for s in description:
#                 if s in punc:
#                     new_str = description.replace(s, "")
#             description = set(new_str.lower().split())
#
#         if filter_words.intersection(requirements.union(description)) == filter_words:
#             new_vacancy = Vacancy(vacancy['name'], vacancy['url'], vacancy['salary'],
#                                     vacancy['requirements'],vacancy['employer'], vacancy['description'])
#             new_list.append(new_vacancy)
#             JSONSaver.add_vacancy('filtered.json', new_vacancy)
#
#     return new_list
#
#
# def sort_by_salary(vacancy):
#     """Функция ключа сортировки"""
#     if vacancy.salary:
#         if vacancy.salary['from']:
#             return vacancy.salary['from']
#     return 0
#
#
# def sort_vacancies(filtered_vacancies):
#     """Функция, сортирующая вакансии по зарплате от большей к меньшей"""
#     filtered_vacancies.sort(key=sort_by_salary, reverse=True)
#     return filtered_vacancies
#
#
# def get_top_vacancies(sorted_vacancies, top_n):
#     """Функция, возвращающая N первых вакансий"""
#     return sorted_vacancies[:top_n]
#
#
# def print_vacancies(vacancies):
#     """Функция печати списка вакансий"""
#     for i in range(len(vacancies)):
#         print(i+1)
#         print(vacancies[i])


def print_employers(data) -> None:
    for employer in data['items']:
        employer_id = employer['id']
        employer_name = employer['name']
        # industries = employer['industries']
        # vacancies_count = employer['open_vacancies']
        print(f"{employer_id} - {employer_name}")


def get_data(hh_employers, hh_vacancies, employers_id_list: list[int]) -> list[dict[str, Any]]:
    """Получение данных из API"""
    data = []
    for employer in hh_employers['items']:
        if int(employer['id']) in employers_id_list:
            vacancies_data = []
            for vacancy in hh_vacancies['items']:
                if vacancy['employer']['id'] == employer['id']:
                    vacancies_data.append(vacancy)
            data.append({'employer': employer, 'vacancies': vacancies_data})
    return data


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных с информацией о вакансиях и работодателях"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE vacancies (
                        id smallint SERIAL PRIMARY KEY,
                        title varchar(100) NOT NULL,
                        employer_id smallint REFERENCES employers(employer_id), 
                        publish_date date NOT NULL,
                        url varchar(100) NOT NULL, 
                        salary_from smallint,
                        salary_to smallint,
                        salary_currency varchar(3)
                        salary_gross boolean,
                        requirements text, 
                        description text
                    )
                """)

            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE employers (
                        employer_id smallint PRIMARY KEY,
                        name NOT NULL,
                        vacancies_count NOT NULL
                    )
                """)
    finally:
        conn.close()


def save_data_to_database(database_name: str, data: list[dict[str, Any]], params: dict) -> None:
    """Сохранение данных в базу данных"""
    conn = psycopg2.connect(dbname=database_name, **params)
    try:
        with conn:
            with conn.cursor() as cur:
                for dictionary in data:
                    employer_data = dictionary['employer']
                    cur.execute(
                        """
                        INSERT INTO employers(employer_id, name, vacancies_count)
                        VALUES (%s, %s, %s)
                        """,
                        (employer_data['id'],
                         employer_data['name'],
                         employer_data['open_vacancies'])
                    )
                    vacancies_data = dictionary['vacancies']
                    for vacancy in vacancies_data:
                        cur.execute(
                            """
                            INSERT INTO vacancies
                            (title, employer_id, publish_date, url, 
                            salary_from, salary_to, salary_currency, salary_gross,
                            requirements, description)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (vacancy['name'],
                             vacancy['employer']['id'],
                             date(vacancy['published_at']),
                             vacancy['alternate_url'],
                             vacancy['salary']['from'],
                             vacancy['salary']['to'],
                             vacancy['salary']['currency'],
                             vacancy['salary']['gross'],
                             vacancy['snippet']['requirement'],
                             vacancy['snippet']['responsibility'])
                        )
    finally:
        conn.close()
