from src.vacancies_API import HeadHunterAPI
from src.functions import filter_vacancies, sort_vacancies, get_top_vacancies, print_vacancies
from src.JSON_processor import JSONSaver

HH_VACANCIES_FILE = "hh_vacancies.json"
HH_EMPLOYERS_FILE = "hh_employers.json"


def main():
    """Функция для взаимодействия с пользователем"""
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()

    # Получение работодателей
    city = input('Введите регион поиска вакансий(город): ')
    hh_employers = hh_api.get_employers(city)
    # Сохранение информации о работодателях в файл
    hh_api.save_employers_to_json(HH_EMPLOYERS_FILE, hh_employers)

    # Получение вакансий по id работодателей
    employer_id = input('Введите id работодателей из списка через запятую: ')
    # 9430380, 3591994, 927820, 3192921, 4069218, 550628, 10138825
    hh_vacancies = hh_api.get_vacancies(employer_id)
    # Сохранение информации о вакансиях в файл
    hh_api.save_vacancies_to_json(HH_VACANCIES_FILE, hh_vacancies)



    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").lower().split()
    # filtered_vacancies = filter_vacancies(HH_VACANCIES_FILE, filter_words)
    #
    # if not filtered_vacancies:
    #     print("Нет вакансий, соответствующих заданным критериям.")
    #     return
    #
    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    #
    # sorted_vacancies = sort_vacancies(filtered_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print("ТОП вакансий:")
    # print_vacancies(top_vacancies)
    # vacancy_to_delete = input("Введите название вакансии, которую будем удалять: ")
    # JSONSaver.delete_vacancy('filtered.json', vacancy_to_delete)
    # salary_from = int(input("Введите минимальную зарплату: "))
    # vacancies_by_salary = JSONSaver.get_vacancies_by_salary(salary_from)
    # print_vacancies(vacancies_by_salary)


if __name__ == "__main__":
    main()
