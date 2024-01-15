from typing import Any
from datetime import datetime
import psycopg2


def print_employers(data) -> None:
    """Вывод списка работодателей"""
    for employer in data['items']:
        employer_id = employer['id']
        employer_name = employer['name']
        # industries = employer['industries']
        # vacancies_count = employer['open_vacancies']
        print(f"{employer_id} - {employer_name}")


def get_data(hh_employers, hh_vacancies, employers_id_list: list[int]) -> list[dict[str, Any]]:
    """Получение списка словарей формата
    {'employer': данные работодателя, 'vacancies': вакансии работодателя}"""
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
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE {database_name}")
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE employers (
                        employer_id int PRIMARY KEY,
                        name varchar(100) NOT NULL,
                        vacancies_count smallint NOT NULL
                    )
                """)
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE vacancies (
                        id SERIAL PRIMARY KEY,
                        title varchar(100) NOT NULL,
                        employer_id int REFERENCES employers(employer_id), 
                        publish_date date NOT NULL,
                        url varchar(100) NOT NULL, 
                        salary_from int,
                        salary_to int,
                        salary_currency varchar(3),
                        salary_gross boolean,
                        requirements text, 
                        description text
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
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (vacancy['name'],
                             vacancy['employer']['id'],
                             datetime.fromisoformat(vacancy['published_at']),
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
