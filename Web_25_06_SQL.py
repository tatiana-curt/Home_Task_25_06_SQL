# Необходимо установить драйвер для обращения к PostgreSQL:$ pip install psycopg2-binary

from pprint import pprint
import psycopg2
from datetime import timedelta, datetime

conn = psycopg2.connect("dbname=test_bd user=postgres password=123456789")

cur = conn.cursor()
cur.execute('''create table cousres_test (id serial primary key, name varchar(100))''')
cur.execute('drop table course')
print(cur.fetchall())

cur = conn.cursor()
now = datetime.now()
long_ago = now - timedelta(days=365*30)
cur.execute('insert into student (name, gpa, birth) values' '(%s,%s, %s)', ('Ivan Ivanov', 4, long_ago))
conn.commit()

print('ОК')
cur.execute("select * from student")
pprint(cur.fetchall())

with psycopg2.connect("dbname=test_bd user=postgres password=123456789") as conn:
    with conn.cursor() as curs:
        now = datetime.now()
        long_ago = now - timedelta(days=365 * 30)
        curs.execute('insert into student (name, gpa, birth) values' '(%s,%s, %s)', ('Ivan Ivanov', 4, long_ago))
        print(curs.fetchall())