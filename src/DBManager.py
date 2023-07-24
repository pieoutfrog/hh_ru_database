import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='hh_ru',
    user='postgres',
    password='9000'
)
class DBManager:
    def __init__(self, **conn_params):
        self.conn_params = conn_params

    def get_companies_and_vacancies_count(self):
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT employer_name, count_open_vacancies FROM employers")
                rows = cur.fetchall()
                for row in rows:
                    employer_name = row[0]  # Извлекаем имя компании из tuple
                    count = row[1]  # Извлекаем количество из tuple
                    print(f"{employer_name}: {count}")  # Выводим имя компании и количество рядом
        # получает список всех компаний и количество вакансий у каждой компании.
        pass

    def get_all_vacancies(self):
        # получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT employer_name, vacancy_name, vacancy_url, salary
FROM employers
INNER JOIN vacancies
USING (employer_id)
WHERE salary IS NOT NULL;""")
                rows = cur.fetchall()
                for row in rows:
                    employer_name = row[0]
                    vacancy_name = row[1]
                    vacancy_url = row[2]
                    salary = row[3]
                    print(f'Имя компании: {employer_name}\nИмя вакансии: {vacancy_name}\nСсылка на вакансию: {vacancy_url}\nЗарпата: {salary}')
                    # employer_name = row[0]  # Извлекаем имя компании из tuple
                    # count = row[1]  # Извлекаем количество из tuple
                    # print(f"{employer_name}: {count}")

    def get_avg_salary(self):
        pass

    # получает среднюю зарплату по вакансиям.

    def get_vacancies_with_higher_salary(self):
        pass

    # получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

    def get_vacancies_with_keyword(self):
        pass
# получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.

db_manager = DBManager(host='localhost', port='5432', dbname='hh_ru', user='postgres', password='9000')

# Вызываем метод get_companies_and_vacancies_count()
# db_manager.get_companies_and_vacancies_count()
db_manager.get_all_vacancies()

