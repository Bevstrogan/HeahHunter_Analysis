from utils import create_database, add_to_table
from db_manager import DBManager

def main():
    employers_list = [8884, 3529, 666661, 1740, 3127, 64174, 856498, 8971731, 2537115, 53742]
    dbmanager = DBManager()
    create_database()
    add_to_table(employers_list)

    while True:
        task = input(
            "\n"
            "-----------------------------------------------------------------------\n"
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

        elif task == '2':
            print(dbmanager.get_all_vacancies())
            print()

        elif task == '3':
            print(dbmanager.get_avg_salary())
            print()

        elif task == '4':
            print(dbmanager.get_vacancies_with_higher_salary())
            print()

        elif task == '5':
            keyword = input('Введите ключевое слово: ')
            print(dbmanager.get_vacancies_with_keyword(keyword))
            print()
        else:
            print('Некорректный запрос')


if __name__ == '__main__':
    main()