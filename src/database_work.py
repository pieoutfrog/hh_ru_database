import requests
import psycopg2


def scrape_employers(company_names, api_key, url):
    """
    Подключение к API, получение данных
    :param company_names: Список названия компаний
    :param api_key: Ключ доступа к API HeadHunter
    :param url: базовая ссылка для просмотра работодателей
    :return: Кортеж с двумя списками. Первый список содержит информацию о компаниях,
        второй список содержит информацию о вакансиях
    """
    employers = []
    vacancies = []
    """
    
    """
    for company_name in company_names:
        params = {
            'text': company_name,
            'access_token': api_key
        }
        response = requests.get(url, params=params)
        data = response.json()

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

    return employers, vacancies


def create_database(database_name: str, db_params: dict):
    """
    Создание БД
    :param database_name: Название создаваемой БД
    :param db_params: Словарь, в котором указаны параметры подключения к базе данных
    """
    conn = psycopg2.connect(**db_params)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE {database_name}")

    cursor.close()
    conn.close()


def create_tables(db_params):
    """
    Создание таблицы в БД
    :param db_params: Словарь, в котором указываются параметры подключения к базе данных
    """
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    create_employers_table_query = '''
            CREATE TABLE IF NOT EXISTS employers (
                employer_id serial PRIMARY KEY,
                employer_name varchar(100) NOT NULL,
                employer_url varchar(100) NOT NULL,
                count_open_vacancies int
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

    try:
        cursor.execute(create_employers_table_query)
        cursor.execute(create_vacancies_table_query)
        conn.commit()
        print("Таблицы успешно созданы")
    except psycopg2.Error as e:
        print("Ошибка при создании таблиц")

    finally:
        conn.close()


def insert_data_to_tables(conn, employers, vacancies):
    """
    Вставка данных о компаниях и вакансиях в соответствующие таблицы базы данных.
    :param conn: Соединение с базой данных.
    :param employers : Список словарей с данными о компаниях.
    :param vacancies: Список словарей с данными о вакансиях.
    """
    with conn:
        with conn.cursor() as cursor:
            for employer in employers:
                insert_employer_query = '''INSERT INTO employers 
                (employer_id, employer_name, employer_url, count_open_vacancies) 
                VALUES (%s, %s, %s, %s)'''
                employer_data = (employer['employer_id'], employer['employer_name'], employer['employer_url'],
                                 employer['count_open_vacancies'])
                cursor.execute(insert_employer_query, employer_data)

            for vacancy in vacancies:
                insert_vacancy_query = '''INSERT INTO vacancies 
                (vacancy_id, vacancy_name, vacancy_url, salary, employer_id) 
                VALUES (%s, %s, %s, %s, %s)'''
                vacancy_data = (
                    vacancy['vacancy_id'], vacancy['vacancy_name'], vacancy['vacancy_url'], vacancy['salary'],
                    vacancy['employer_id'])
                cursor.execute(insert_vacancy_query, vacancy_data)

        conn.commit()
