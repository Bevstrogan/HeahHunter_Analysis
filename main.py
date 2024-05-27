from utils import create_database, add_to_table
from db_manager import DBManager

def main():
    employers_list = []
    dbmanager = DBManager()
    create_database()
    add_to_table(employers_list)

    while True:
        task = input(
            "----------------------------Здравствуйте---------------------------\n"
            "1 - Список всех компаний и количество их вакансий\n"
            "2 - Список всех вакансий с указанием названия компании\n"
            "3 - Получить среднюю зарплату по вакансиям\n"
            "4 - Список всех вакансий с зарплатой выше средней по всем вакансиям\n"
            "5 - Список вакансий в которых есть переданное слово\n"
            "Стоп - Завершить работу программы\n"
            "Введите команду: "
        )

        if task == 'Стоп':
            break

        if task == '1':
            print(dbmanager.get_companyies_and_vacancies_count())
            print()

        if task == '2':
            print(dbmanager.get_all_vacancies())
            print()

        if task == '3':
            print(dbmanager.get_avg_salary())
            print()

        if task == '4':
            print(dbmanager.get_vacancies_with_higher_salary())
            print()

        if task == '5':
            print(dbmanager.get_vacancies_with_keyword())
            print()
        else:
            print('Некорректный запрос')


if __name__ == '__main__':
    main()