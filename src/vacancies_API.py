import json
from abc import ABC, abstractmethod
import requests
from src.JSON_processor import JSONSaver
from src.vacancy import Vacancy
from src.employer import Employer


class VacanciesAPI(ABC):

    @abstractmethod
    def get_vacancies(self, name):
        pass

    @abstractmethod
    def save_vacancies_to_json(self):
        pass

    @abstractmethod
    def get_employers(self):
        pass

    @abstractmethod
    def save_employers_to_json(self):
        pass


class HeadHunterAPI(VacanciesAPI):
    vacancies_url = 'https://api.hh.ru/vacancies'
    employers_url = 'https://api.hh.ru/employers'

    def get_vacancies(self, employers_id_list: list[int]):
        """Получает вакансии с сайта"""
        response = requests.get(self.vacancies_url, params={'employer_id': employers_id_list, 'per_page': 100})
        # print(response.json())
        return response.json()

    def get_employers(self, city: str):
        """Получает информацию о работодателях с сайта"""
        response = requests.get(self.employers_url, params={'text': city, 'only_with_vacancies': True, 'per_page': 100})
        # print(response.json())
        return response.json()

    def save_vacancies_to_json(self, filename, data) -> None:
        """Сохраняет вакансии в файл"""
        for vacancy in data['items']:
            name = vacancy['name']
            url = vacancy['alternate_url']
            salary = vacancy['salary']
            requirements = vacancy['snippet']['requirement']
            employer = vacancy['employer']['name']
            description = vacancy['snippet']['responsibility']
            new_vacancy = Vacancy(name, url, salary, requirements, employer, description)
            JSONSaver.add_vacancy('hh_vacancies.json', new_vacancy)

    def save_employers_to_json(self, filename, data) -> None:
        """Сохраняет информацию о работодателях в файл"""
        for employer in data['items']:
            employer_id = employer['id']
            name = employer['name']
            # industries = employer['industries']
            vacancies_count = employer['open_vacancies']
            new_employer = Employer(employer_id, name, vacancies_count)
            JSONSaver.add_vacancy(filename, new_employer)
            print(new_employer)
