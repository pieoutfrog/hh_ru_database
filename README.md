# hh_ru_database
**HH.ru Database**

Этот проект представляет собой скрипт на языке Python, который взаимодействует с базой данных PostgreSQL для получения и анализа данных с сайта hh.ru. 
Он позволяет получать информацию о компаниях, вакансиях и зарплатах.

**Описание**

**Основные функции программы включают:**

* `get_all_vacancies`: Получает и выводит информацию о всех вакансиях, включая имя компании, имя вакансии, ссылку на вакансию и зарплату (если указана).
* `get_avg_salary`: Получает и выводит среднюю зарплату для каждой компании.
* `get_vacancies_with_higher_salary`: Получает и выводит информацию о вакансиях с зарплатой выше средней.
* `get_vacancies_with_keyword`: Получает и выводит информацию о вакансиях, содержащих определенное ключевое слово.

**Установка и использование**

Для установки и запуска программы выполните следующие шаги:
* Клонируйте репозиторий: git clone https://github.com/pieoutfrog/hh_ru_database.git
* Установите необходимые зависимости: pip install -r requirements.txt
* Настройте базу данных PostgreSQL:
   - Создайте новую базу данных в PostgreSQL.
   - Обновите параметры подключения в файле `hh_database.py` с учетом ваших учетных данных для базы данных PostgreSQL.

**Требования**

* Python 3.6 или выше
* Установленные зависимости, указанные в файле requirements.txt
* Python 3.x
* PostgreSQL
* библиотека psycopg2

**Контрибуция**

Вклад приветствуется! Если вы обнаружили ошибки или у вас есть предложения по улучшению, пожалуйста, откройте issue или отправьте pull request.