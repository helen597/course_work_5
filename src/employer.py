class Employer:
    def __init__(self, employer_id, name, vacancies_count):
        self.id = employer_id
        self.name = name
        # self.industries = industries
        self.vacancies_count = vacancies_count

    def __str__(self):
        return f'{self.id} - {self.name}'
        # ({self.industries})'

    def __dict__(self):
        return {'id': self.id,
                'name': self.name,
                # 'industries': self.industries,
                'vacancies_count': self.vacancies_count}
