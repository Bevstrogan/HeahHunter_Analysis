import psycopg2

class DBManager:
    """Класс для подключения к базе данных"""
    def get_companyies_and_vacancies_count(self):
        """Метод для получения компаний и количества их вакансий"""

        with psycopg2.connect(
                host="localhost",
                database="headhunter_database",
                user="postgres",
                password="0835"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT company_name, COUNT(vacancies_name) AS count_vacancies "
                            f"FROM employers "
                            f"JOIN vacancies USING (employer_id) "
                            f"GROUP BY employers.company_name")
                result = cur.fetchall()
            conn.commit()
        return result

    def get_all_vacancies(self):
        """Метод для получения списка всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию"""
        with psycopg2.connect(
                host="localhost",
                database="headhunter_database",
                user="postgres",
                password="0835"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT employers.company_name, vacancies.vacancies_name, "
                            f"vacancies.payment, vacancies_url "
                            f"FROM employers "
                            f"JOIN vacancies USING (employer_id)")
                result = cur.fetchall()
            conn.commit()
        return result

    def get_avg_salary(self):
        """Метод для получения средней зарплаты по вакансиям"""
        with psycopg2.connect(
                host="localhost",
                database="headhunter_database",
                user="postgres",
                password="0835"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT AVG(payment) as avg_payment FROM vacancies")
                result = cur.fetchall()
            conn.commit()
        return result

    def get_vacancies_with_higher_salary(self):
        """Метод для получения вакансий с зарплатой выше средней по всем вакансиям"""
        with psycopg2.connect(
                host="localhost",
                database="headhunter_database",
                user="postgres",
                password="0835"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancies "
                            f"WHERE payment > (SELECT AVG(payment) FROM vacancies)")
                result = cur.fetchall()
            conn.commit()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Метод для поиска вакансий по ключевым словам"""
        with psycopg2.connect(
                host="localhost",
                database="headhunter_database",
                user="postgres",
                password="0835"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancies "
                            f"WHERE lower(vacancies_name) LIKE '%{keyword}%' "
                            f"OR lower(vacancies_name) LIKE '%{keyword}' "
                            f"OR lower(vacancies_name) LIKE '{keyword}%';")
                result = cur.fetchall()
            conn.commit()
        return result