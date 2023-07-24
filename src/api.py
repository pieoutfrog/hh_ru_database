import requests
import psycopg2

company_names = ['Яндекс', 'Digital Reputation', 'Ozon Fintech', 'SberTech', 'ЛАНИТ',
                 'VK', 'Альфа-Банк', 'Lamoda Tech', 'Тинькофф', 'KVINT']

api_key = 'hh_api'
url = 'https://api.hh.ru/employers'
for company_name in company_names:
    params = {
        'text': company_name,
        'access_token': api_key  # Ваш API-ключ
    }
    # Отправляем GET-запрос к API hh.ru
    response = requests.get(url, params=params)
    data = response.json()

    employers = []
    vacancies = []
    for company in data['items']:
        if company['open_vacancies'] != 0:
            employer_id = company['id']
            vacancies_url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
            employer_name = company['name']
            employer_url = company['alternate_url']
            count_open_vacancies = company['open_vacancies']
            response = requests.get(vacancies_url, params={'access_token': api_key})
            vacancies_data = response.json()
            employers.append({
                'employer_id': employer_id,
                'employer_name': employer_name,
                'employer_url': employer_url,
                'count_open_vacancies': count_open_vacancies
            })
            for vacancy in vacancies_data['items']:

                vacancy_name = vacancy['name']
                vacancy_url = vacancy['alternate_url']
                vacancies.append({
                    'employer_id': employer_id,
                    'vacancy_name': vacancy_name,
                    'vacancy_url': vacancy_url,
                    'salary': vacancy['salary']['from'] if vacancy['salary'] is not None else None,
                    'vacancy_id': vacancy['id']
                })
    conn = psycopg2.connect(
        host='localhost',
        database='hh_ru',
        user='postgres',
        password='9000'
    )

    try:
        # Создание таблицы "employers"
        create_employers_table_query = '''
    CREATE TABLE IF NOT EXISTS employers (
        employer_id serial PRIMARY KEY,
        employer_name varchar(100) NOT NULL,
        employer_url varchar(100) NOT NULL,
        open_vacancies int
    )
    '''

        create_vacancies_table_query = '''
    CREATE TABLE IF NOT EXISTS vacancies (
        vacancy_id serial PRIMARY KEY,
        vacancy_name varchar(100) NOT NULL,
        vacancy_url varchar(100) NOT NULL,
        salary int,
        employer_id int REFERENCES employers(employer_id)
    )
    '''

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(create_employers_table_query)
                cursor.execute(create_vacancies_table_query)

            # Вставка данных о работодателях
            for employer in employers:
                insert_employer_query = "INSERT INTO employers (employer_id, employer_name, employer_url, count_open_vacancies) VALUES (%s, %s, %s, %s)"
                employer_data = (employer['employer_id'], employer['employer_name'], employer['employer_url'], employer['count_open_vacancies'])
                with conn.cursor() as cursor:
                    cursor.execute(insert_employer_query, employer_data)


            # Вставка данных о вакансиях
            for vacancy in vacancies:
                insert_vacancy_query = "INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_url, salary, employer_id) VALUES (%s, %s, %s, %s, %s)"
                vacancy_data = (
                    vacancy['vacancy_id'], vacancy['vacancy_name'], vacancy['vacancy_url'], vacancy['salary'],
                    vacancy['employer_id'])
                with conn.cursor() as cursor:
                    cursor.execute(insert_vacancy_query, vacancy_data)

            conn.commit()
    finally:
        conn.close()
