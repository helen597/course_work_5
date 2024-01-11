class Vacancy:
    def __init__(self, name, url, salary, requirements, employer, description=''):
        self.name = name
        self.employer = employer
        self.url = url
        self.salary = salary
        self.requirements = requirements
        self.description = description

    def __str__(self):
        info = f'{self.name}\n{self.employer}\n'
        if self.salary:
            info += 'Зарплата '
            # print(f'\n{self.salary}\n')
            if self.salary['from']:
                info += f"от {self.salary['from']} "
            if self.salary['to']:
                info += f"до {self.salary['to']} "
            if self.salary['currency'] == 'RUR' or self.salary['currency'] == 'rub':
                info += f"рублей "
            else:
                info += f"{self.salary['currency']} "
            if self.salary['gross']:
                info += f'до вычета налогов'
            info += '\n'
        if self.requirements:
            requirements = "Требования: " + self.requirements.replace(". ", ".\n")
            info += f'{requirements}\n'
        if self.description:
            description = "Обязанности: " + self.description.replace(". ", ".\n")
            info += f'{description}\n'
        info += f'{self.url}\n'
        return info

    def __dict__(self):
        return {'name': self.name,
                'employer': self.employer,
                'url': self.url,
                'salary': self.salary,
                'requirements': self.requirements,
                'description': self.description}

    def __lt__(self, other):
        return self.salary < other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __ge__(self, other):
        return self.salary >= other.salary

    def __eq__(self, other):
        return self.salary == other.salary
