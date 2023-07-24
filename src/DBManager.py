import psycopg2


class DBManager:
    def __init__(self, **conn_params):
        self.conn_params = conn_params

    def get_companies_and_vacancies_count(self):
        """
        Получает и выводит информацию о компаниях и количестве открытых вакансий из таблицы employers.
        """
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT employer_name, count_open_vacancies FROM employers")
                rows = cur.fetchall()
                for row in rows:
                    employer_name = row[0]  # Извлекаем имя компании из tuple
                    count = row[1]  # Извлекаем количество из tuple
                    print(
                        f"Имя компании:{employer_name}, число открытых вакансий: {count}")

    def get_all_vacancies(self):
        """
        Получает и выводит информацию о всех вакансиях из таблицы vacancies,
        включая имя компании, имя вакансии, ссылку на вакансию и зарплату (если указана).
        """
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
                    print(
                        f'Имя компании: {employer_name}\nИмя вакансии: {vacancy_name}\nСсылка на вакансию: {vacancy_url}\nЗарпата: {salary}')

    def get_avg_salary(self):
        """
        Получает и выводит информацию о средней зарплате в каждой компании из таблицы vacancies.
        """
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT employers.employer_name, ROUND(AVG(vacancies.salary))
FROM vacancies
JOIN employers USING (employer_id)
GROUP BY employers.employer_name''')
                rows = cur.fetchall()
                for row in rows:
                    employer_name = row[0]
                    avg_salary = row[1]
                    if avg_salary is not None:
                        print(f'Средняя зарплата в компании {employer_name}: {avg_salary}')

                    else:
                        print(f'Среднюю зарплату в компании {employer_name} невозможно вычислить')

    def get_vacancies_with_higher_salary(self):
        """
        Получает и выводит информацию о вакансиях, у которых зарплата выше средней по всем вакансиям.
        """
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT vacancies.vacancy_name, vacancies.salary, employers.employer_name
                FROM vacancies
                JOIN employers ON vacancies.employer_id = employers.employer_id
                WHERE vacancies.salary > (SELECT AVG(salary) FROM vacancies)''')
                rows = cur.fetchall()
                for row in rows:
                    vacancy_name = row[0]
                    salary = row[1]
                    employer_name = row[2]
                    print(f'Имя компании: {employer_name};\n Вакансия: {vacancy_name};\n Зарплата: {salary}')

    def get_vacancies_with_keyword(self):
        """Получает ключевое слово от пользователя и выводит информацию
        о вакансиях, содержащих это ключевое слово."""
        keyword = input("Введите ключевое слово: ")
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f'''SELECT vacancies.vacancy_name, vacancies.salary, employers.employer_name FROM vacancies
    JOIN employers ON vacancies.employer_id = employers.employer_id 
    WHERE vacancy_name ILIKE '%{keyword}%'
    ''')
                rows = cur.fetchall()
                for row in rows:
                    vacancy_name = row[0]
                    salary = row[1]
                    employer_name = row[2]
                    if salary is not None:
                        print(f'Компания: {employer_name}, {vacancy_name}, зарплата: {salary}')
                    else:
                        print(f'Компания: {employer_name}, {vacancy_name}, зарплата: не указана')
