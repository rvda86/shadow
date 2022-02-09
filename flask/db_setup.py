from mysql.connector import connect, Error
from shadow.db_mysql import db_pool
from shadow import DB_USER, DB_PASSWORD

db = db_pool.acquire()

def create_db(name):
    try:
        with connect(
            host="localhost",
            user=DB_USER,
            password=DB_PASSWORD
        ) as connection:
            create_db_query = f"CREATE DATABASE {name}"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)

def create_tables():
    create_tables_sql = [db.create_table_users_sql, db.create_table_categories_sql, db.create_table_topics_sql,
                        db.create_table_journal_entries_sql, db.create_table_todo_entries_sql]
    for sql in create_tables_sql:
        db.create_table(sql)

def drop_db(name):
    try:
        with connect(
            host="localhost",
            user=DB_USER,
            password=DB_PASSWORD
        ) as connection:
            create_db_query = f"DROP DATABASE IF EXISTS {name}"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)

if __name__ == '__main__':
    # create_db(db.name)
    # create_tables()
    # drop_db('shadow_dev')
    pass