import psycopg2
from src.config import config
DATABASE_NAME = 'headhunter'


class DBManager:

    def __init__(self):
        self.params = config()
        self.conn = psycopg2.connect(dbname=DATABASE_NAME, **self.params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        self.cur.execute(
            """
            SELECT * FROM employers
            """)
        result = self.cur.fetchall()
        return result

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        self.cur.execute(
            """
            SELECT employers.name, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.salary_currency, vacancies.salary_gross, vacancies.url
            FROM vacancies
            JOIN employers
            USING(employer_id)
            """)
        result = self.cur.fetchall()
        return result

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        self.cur.execute(
            """
            SELECT AVG(salary_from)
            FROM vacancies
            """)
        result = self.cur.fetchall()
        return result

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.cur.execute(
            """
            SELECT *
            FROM vacancies
            WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
            ORDER BY salary_from
            """)
        result = self.cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        self.cur.execute(
            f"""
            SELECT *
            FROM vacancies
            WHERE {keyword} IN name
            """)
        result = self.cur.fetchall()
        return result
