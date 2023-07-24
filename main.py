import psycopg2
from src.database_work import scrape_employers, create_tables, insert_data_to_tables, create_database
from src.DBManager import DBManager

company_names = ['Яндекс', 'Digital Reputation', 'Ozon Fintech', 'SberTech', 'ЛАНИТ',
                 'VK', 'Альфа-Банк', 'Lamoda Tech', 'Тинькофф', 'KVINT']

api_key = 'hh_api'
url = 'https://api.hh.ru/employers'
params = {
    'host': 'localhost',
    'database': 'hh_ru',
    'user': 'postgres',
    'password': '9000'
}
db_params = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '9000'
}
database_name = 'hh_ru'
conn = psycopg2.connect(
    host='localhost',
    database=database_name,
    user='postgres',
    password='9000'
)
# создание базы данных, получение данных, создание таблиц и заполнение их данными
create_database(database_name, db_params)
employers, vacancies = scrape_employers(company_names, api_key, url)
create_tables(params)
insert_data_to_tables(conn, employers, vacancies)

# пример использования класса DBManager
db_manager = DBManager(host='localhost', port='5432', dbname='hh_ru', user='postgres', password='9000')
db_manager.get_avg_salary()
db_manager.get_vacancies_with_keyword()
db_manager.get_all_vacancies()
db_manager.get_companies_and_vacancies_count()
db_manager.get_vacancies_with_higher_salary()
