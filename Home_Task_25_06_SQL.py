from pprint import pprint
import psycopg2
from datetime import timedelta, datetime
from random import randint

# !!! Вопросы:
# 1. Как вставлять переменные в запрос не через format() а через (%s), если это не переменные для записи в БД (которые передаются в value),
# а просто название таблиц в запросе? или если это не переменные для записи в БД, то можно через format()?

# 2. Как сформировать запрос на создание вспомогательной таблицы "students_courses" чтобы нельзя было записать одного и того же студента на один и тот же курс,
# т.е. исключит возможность создания одинаковой пары "student_id" и "course_id"?

# 3. Как написать декоратор Для всех функций, который бы подключался к БД и передавал курсор?? Это поможет не конектиться к БД в каждой функции?_
# def connect_db(old_function):
#     def new_function(*args, **kwargs):
#         with psycopg2.connect("dbname=test_bd user=postgres password=123456789") as conn:
#             with conn.cursor() as curs:
#                 return curs
#     return new_function


# Данные для подключения к БД
params = {
    'dbname': 'test_bd',
    'user': 'postgres',
    'password': '123456789'
}

def create_db(*args): # создает таблицы
    list_name_table = list(args)
    with psycopg2.connect("dbname={} user={} password={}".format(params['dbname'], params['user'], params['password'])) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute('''create table {} (id serial primary key, name character varying(100) not null unique)'''.format(list_name_table[0]))
                curs.execute('''create table {} (id serial primary key, name character varying(100) not null unique, gpa numeric(10,2), birth timestamp with time zone)'''.format(list_name_table[1]))
                curs.execute('''create table {} (id serial primary key, student_id integer references {}(id), course_id integer references {}(id))'''.format(list_name_table[2], list_name_table[1], list_name_table[0]))
            except psycopg2.errors.DuplicateTable as e:
                print(e)


def add_courses(*args):  # создает курсы
    list_name_courses = list(args)
    with psycopg2.connect("dbname={} user={} password={}".format(params['dbname'], params['user'], params['password'])) as conn:
        with conn.cursor() as curs:
            try:
                for name_course in list_name_courses:
                    curs.execute('insert into {} (name) values' '(%s)'.format(name_table_course), [name_course])
            except psycopg2.errors.UniqueViolation as e:
                print(e)

def get_students(course_id): # возвращает студентов определенного курса
    with psycopg2.connect("dbname={} user={} password={}".format(params['dbname'], params['user'], params['password'])) as conn:
        with conn.cursor() as curs:
            curs.execute("select {}.name from {} "
                         "join {} on {}.student_id = {}.id "
                         "join {} on {}.course_id = {}.id "
                         "where {}.id = '3'".format(name_table_student,
                                                    name_table_student_courses,
                                                    name_table_student,
                                                    name_table_student_courses,
                                                    name_table_student,
                                                    name_table_course,
                                                    name_table_student_courses,
                                                    name_table_course,
                                                    name_table_course))
            return (curs.fetchall())


def add_students(name_students, course_id): # создает студентов и # записывает их на курс
    add_student(name_students)
    id_student = get_ID_student(name_students)
    # print(id_student)
    with psycopg2.connect("dbname={} user={} password={}".format(params['dbname'], params['user'], params['password'])) as conn:
        with conn.cursor() as curs:
            curs.execute('insert into {} (student_id, course_id) values' '(%s, %s)'.format(name_table_student_courses), (id_student, course_id))


def get_ID_student(name_student): # получаем ID студента
    with psycopg2.connect("dbname={} user={} password={}".format(params['dbname'], params['user'], params['password'])) as conn:
        with conn.cursor() as curs:
            curs.execute('''select id from {} where name like '{}' '''.format(name_table_student, name_student))
            return (curs.fetchall()[0][0])


def add_student(*args): # просто создает студентов
    list_name_students = list(args)
    now = datetime.now()
    long_ago = now - timedelta(days=365 * 10)
    gpa = randint(1, 5)
    with psycopg2.connect("dbname={} user={} password={}".format(params['dbname'], params['user'], params['password'])) as conn:
        with conn.cursor() as curs:
            try:
                for name_student in list_name_students:
                    curs.execute('insert into {} (name, gpa, birth) values' '(%s, %s, %s)'.format(name_table_student), (name_student, gpa, long_ago))
            except psycopg2.errors.UniqueViolation as e:
                print(e)


def get_student(student_id): # найти студента по ID
    with psycopg2.connect("dbname={} user={} password={}".format(params['dbname'], params['user'], params['password'])) as conn:
        with conn.cursor() as curs:
            curs.execute(''' select * from {} where id='{}' '''.format(name_table_student, student_id))
            return (curs.fetchall()[0])

# _______________________________________________________________________________________________________________________________________________________________________
# Создаем 3 таблицы 'name_table_course', 'name_table_student', 'name_table_student_courses'
name_table_course = 'courses'
name_table_student = 'students'
name_table_student_courses = 'students_courses'
create_db(name_table_course, name_table_student, name_table_student_courses)

# Создаем студента (студентов)
add_student('Ivan Ivanov', 'Mari Zolotova')

# Создаем объекты (курсы): "python", "SMM", "Java", "C++"
add_courses('python', 'SMM', 'Java', 'C++')
# add_courses('C#')

# Создаем студента 'Tatiana Petruk' и записываем его на курс c ID=3
add_students('Tatiana Petruk', 3)
add_students('Anna Zolotova', 3)

# Получит студента по ID
print(get_student(1))

# Возвращает студентов определенного курса (ID=3)
print(get_students(3))


# Примечания:
# для кодировки в консоли: В командной строке помогло перед запуском psql выполнить chcp 1251