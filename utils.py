import psycopg2
import requests

def get_vacancies(employer_id):
    """Получение вакансий по API"""

    params = {
        "area": 1,
        "page": 0,
        "per_page": 10
    }
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    data_vacancies = requests.get(url, params=params).json()

    vacancies_data = []
    for vacancy in data_vacancies["items"]:
        vacancies = {
            'vacancy_id': int(vacancy['id']),
            'vacancies_name': vacancy['name'],
            'payment': vacancy["salary"]["from"] if vacancy["salary"] else None,
            'requirement': vacancy['snippet']['requirement'],
            'vacancies_url': vacancy['alternate_url'],
            'employer_id': employer_id
        }
        if vacancies['payment'] is not None:
            vacancies_data.append(vacancies)

        return vacancies_data

def get_employer(employer_id):
    """Получение данных о работодателе"""

    url = f"https://api.hh.ru/employers/{employer_id}"
    data_vacancies = requests.get(url).json()
    company_data = {
        "employer_id": int(employer_id),
        "company_name": data_vacancies['name'],
        "open_vacancies": data_vacancies["open_vacancies"]
    }
    return company_data

def create_database():
    """Создание бд и таблиц"""

    conn = psycopg2.connect(
        host="localhost",
        database="test",
        user="postgres",
        password="0835"
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("DROP DATABASE IF EXISTS headhunter_database")
    cur.execute("CREATE DATABASE headhunter_database")

    conn.close()

    conn = psycopg2.connect(
        host="localhost",
        database="headhunter_database",
        user="postgres",
        password="0835"
    )

    with conn.cursor() as cur:
        cur.execute('''
                    CREATE TABLE employers (
                    employer_id INTEGER PRIMARY KEY,
                    company_name varchar(255),
                    open_vacancies INTEGER
                    )''')

        cur.execute('''
                    CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    vacancies_name varchar(255),
                    payment INTEGER,
                    requirement TEXT,
                    vacancies_url TEXT,
                    employer_id INTEGER REFERENCES employers(employer_id)
                    )''')
    conn.commit()
    conn.close()

def add_to_table(employers_list):
    """Заполнение бд данными"""

    with psycopg2.connect(
        host="localhost",
        database="headhunter_database",
        user="postgres",
        password="0835"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE employers, vacancies RESTART IDENTITY;')
            for employer in employers_list:
                employer_list = get_employer(employer)
                cur.execute('INSERT INTO employers (employer_id, company_name, open_vacancies) '
                            'VALUES (%s, %s, %s) RETURNING employer_id',
                            (employer_list['employer_id'], employer_list['company_name'],
                             employer_list['open_vacancies']))
            for employer in employers_list:
                vacancy_list = get_vacancies(employer)
                for vacancy in vacancy_list:
                    cur.execute('INSERT INTO vacancies (vacancy_id, vacancies_name, '
                                'payment, requirement, vacancies_url, employer_id) '
                                'VALUES (%s, %s, %s, %s, %s, %s)',
                                (vacancy['vacancy_id'], vacancy['vacancies_name'], vacancy['payment'],
                                 vacancy['requirement'], vacancy['vacancies_url'], vacancy['employer_id']))

    conn.commit()