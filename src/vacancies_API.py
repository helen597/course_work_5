from abc import ABC, abstractmethod
import requests


class VacanciesAPI(ABC):

    @abstractmethod
    def get_vacancies(self, name):
        pass


    @abstractmethod
    def get_employers(self):
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
