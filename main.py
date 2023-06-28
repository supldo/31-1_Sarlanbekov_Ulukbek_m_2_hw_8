import sqlite3

# Функция для подключения к БД
def create_connect(db_name):
    connect = None
    try:
        connect = sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
    return connect

# Функция для запроса данных из БД
def select_sql(connect, sql):
    try:
        curses = connect.cursor()
        curses.execute(sql)
        data = curses.fetchall()
        return data
    except sqlite3.Error as e:
        print(e)

# Название БД
database = 'hw.db'

# Подключение к БД
connection = create_connect(database)

if connection:
    while True:
        print('Вы можете отобразить список сотрудников по выбранному id города из перечня городов ниже, '
              'для выхода из программы введите 0:')

        # Запрос всех городов из БД
        cities_sql = '''
        SELECT id, title FROM cities
        '''
        cities = select_sql(connection, cities_sql)

        # Распечатка всех городов
        for id, title in cities:
            print(f'{id}: {title}')

        # Ввод данных от пользователя
        select_user = input('Выберите: ')

        # Завершение программы
        if not select_user:
            print('Вы вышли из программы!')
            break

        # Запрос всех сотрудников по выбронному городу из БД
        employees_sql = f'''
        SELECT em.first_name, em.last_name, co.title, ci.title, ci.area FROM employees as em
        LEFT JOIN cities as ci on ci.id == em.city_id
        LEFT JOIN countries as co on co.id == ci.country_id
        WHERE ci.id == {select_user}
        '''
        employees = select_sql(connection, employees_sql)

        # Распечатка результата
        if employees:
            print('Список все сотрудников из этого города')
        else:
            print('Нету сотрдников из этого города')

        count = 1
        for first_name, last_name, country, city, area in employees:
            print(f'{count}: {first_name} {last_name}, {country}, {city}, {area} км²')
            count += 1

        print('----------------------------------------------------------------------')

