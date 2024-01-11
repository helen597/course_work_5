from abc import ABC, abstractmethod
import json, os
from src.vacancy import Vacancy


class FileProcessor(ABC):

    @abstractmethod
    def add_vacancy(self):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self):
        pass


class JSONSaver(FileProcessor):

    def __init__(self):
        pass

    @staticmethod
    def add_vacancy(filename, vacancy):
        """Добавляет вакансию в файл"""
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([vacancy.__dict__()], f, ensure_ascii=False)
        else:
            with open(filename, 'r', encoding='utf-8') as f:
                content = json.load(f)
                content.append(vacancy.__dict__())
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False)

    @staticmethod
    def delete_vacancy(filename, vacancy_name):
        """Удаляет вакансию из файла по имени"""
        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
        content_copy = content.copy()
        for i in range(len(content)):
            # print(content[i])
            if content[i]['name'] == vacancy_name:
                del content_copy[i]
                print("Вакансия удалена")
                break
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content_copy, f, ensure_ascii=False)

    @staticmethod
    def get_vacancies_by_salary(salary_from):
        """Находит вакансии в зависимости от указанной минимальной зарплаты"""
        new_list = []
        if os.path.exists('filtered_by_salary.json'):
            with open('filtered_by_salary.json', 'w', encoding='utf-8') as f:
                json.dump(new_list, f, ensure_ascii=False)

        with open('filtered.json', 'r', encoding='utf-8') as f:
            content = json.load(f)

        for vacancy in content:
            if vacancy['salary']:
                if vacancy['salary']['from']:
                    if vacancy['salary']['to']:
                        if vacancy['salary']['to'] >= salary_from:
                            new_vacancy = Vacancy(vacancy['name'], vacancy['url'], vacancy['salary'],
                                                  vacancy['requirements'], vacancy['employer'], vacancy['description'])
                            new_list.append(new_vacancy)
                            JSONSaver.add_vacancy('filtered_by_salary.json', new_vacancy)
                    else:
                        if vacancy['salary']['from'] + 5 >= salary_from:
                            new_vacancy = Vacancy(vacancy['name'], vacancy['url'], vacancy['salary'],
                                                  vacancy['requirements'], vacancy['employer'], vacancy['description'])
                            new_list.append(new_vacancy)
                            JSONSaver.add_vacancy('filtered_by_salary.json', new_vacancy)
                else:
                    if vacancy['salary']['to']:
                        if vacancy['salary']['to'] >= salary_from:
                            new_vacancy = Vacancy(vacancy['name'], vacancy['url'], vacancy['salary'],
                                                  vacancy['requirements'], vacancy['employer'], vacancy['description'])
                            new_list.append(new_vacancy)
                            JSONSaver.add_vacancy('filtered_by_salary.json', new_vacancy)
        return new_list
