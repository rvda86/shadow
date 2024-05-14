from mysql.connector import connect, Error
from app.db_mysql import db_pool
from app.config import Config

db = db_pool.acquire()

def create_db(name):
    try:
        with connect(
            host="localhost",
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        ) as connection:
            create_db_query = f"CREATE DATABASE {name}"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)

create_table_users_sql =    """CREATE TABLE IF NOT EXISTS users (
                                id CHAR(36) PRIMARY KEY,
                                username VARCHAR(100) NOT NULL UNIQUE,
                                email VARCHAR(100) NOT NULL UNIQUE,
                                password VARCHAR(100) NOT NULL,
                                email_verified BOOLEAN NOT NULL DEFAULT 0
                            );"""

create_table_categories_sql = """CREATE TABLE IF NOT EXISTS categories (
                                id CHAR(36) PRIMARY KEY,
                                user_id CHAR(36) NOT NULL,
                                name VARCHAR(100) NOT NULL,
                                FOREIGN KEY(user_id) REFERENCES users(id) on DELETE RESTRICT
                            );"""

create_table_topics_sql =   """CREATE TABLE IF NOT EXISTS topics (
                                id CHAR(36) PRIMARY KEY,
                                user_id CHAR(36) NOT NULL,
                                category_id CHAR(36) NOT NULL,
                                name VARCHAR(100) NOT NULL,
                                topic_type VARCHAR(100) NOT NULL,
                                FOREIGN KEY(user_id) REFERENCES users(id) on DELETE RESTRICT,
                                FOREIGN KEY(category_id) REFERENCES categories(id) on DELETE RESTRICT
                            );"""

create_table_journal_entries_sql =  """CREATE TABLE IF NOT EXISTS journal_entries (
                                id CHAR(36) PRIMARY KEY,
                                user_id CHAR(36) NOT NULL,
                                topic_id CHAR(36) NOT NULL,
                                date_posted DATETIME(0) NOT NULL,
                                date_edited DATETIME(0),
                                title VARCHAR(100) NOT NULL,
                                content TEXT,                           
                                FOREIGN KEY(user_id) REFERENCES users(id) on DELETE RESTRICT,
                                FOREIGN KEY(topic_id) REFERENCES topics(id) on DELETE RESTRICT
                            );"""

create_table_todo_entries_sql =  """CREATE TABLE IF NOT EXISTS todo_entries (
                                id CHAR(36) PRIMARY KEY,
                                user_id CHAR(36) NOT NULL,
                                topic_id CHAR(36) NOT NULL,
                                date_posted DATETIME(0) NOT NULL,
                                date_edited DATETIME(0),
                                task VARCHAR(100) NOT NULL,
                                completed BOOLEAN NOT NULL DEFAULT 0,                           
                                FOREIGN KEY(user_id) REFERENCES users(id) on DELETE RESTRICT,
                                FOREIGN KEY(topic_id) REFERENCES topics(id) on DELETE RESTRICT
                            );"""

create_table_habit_entries_sql =  """CREATE TABLE IF NOT EXISTS habit_entries (
                                id CHAR(36) PRIMARY KEY,
                                user_id CHAR(36) NOT NULL,
                                topic_id CHAR(36) NOT NULL,
                                date_posted DATETIME(0) NOT NULL,
                                date_edited DATETIME(0),
                                name VARCHAR(100) NOT NULL,                           
                                FOREIGN KEY(user_id) REFERENCES users(id) on DELETE RESTRICT,
                                FOREIGN KEY(topic_id) REFERENCES topics(id) on DELETE RESTRICT
                            );"""

create_table_habit_days_completed_sql = """CREATE TABLE IF NOT EXISTS habit_days_completed (
                                user_id CHAR(36) NOT NULL,
                                habit_id CHAR(36) NOT NULL,
                                day CHAR(14) NOT NULL,                         
                                FOREIGN KEY(user_id) REFERENCES users(id),
                                FOREIGN KEY(habit_id) REFERENCES habit_entries(id) on DELETE CASCADE,
                                PRIMARY KEY(habit_id, day)
                            );"""

create_table_tags_sql =     """CREATE TABLE IF NOT EXISTS tags (
                                id CHAR(36) PRIMARY KEY,
                                user_id CHAR(36) NOT NULL,
                                tag VARCHAR(100) NOT NULL,
                                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                                UNIQUE(user_id, tag)                              
                            );"""

create_table_journal_tags_sql = """CREATE TABLE IF NOT EXISTS journal_tags (
                                id CHAR(36) PRIMARY KEY,
                                user_id CHAR(36) NOT NULL,
                                tag_id CHAR(36) NOT NULL,
                                journal_id CHAR(36) NOT NULL,
                                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                                FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE,
                                FOREIGN KEY(journal_id) REFERENCES journal_entries(id), 
                                UNIQUE(tag_id, journal_id)                              
                            );"""

def create_tables():
    create_tables_sql = [create_table_users_sql, 
                        create_table_categories_sql, 
                        create_table_topics_sql,
                        create_table_journal_entries_sql, 
                        create_table_todo_entries_sql,
                        create_table_habit_entries_sql,
                        create_table_habit_days_completed_sql,
                        create_table_tags_sql,
                        create_table_journal_tags_sql
                        ]

    for sql in create_tables_sql:
        db.create_table(sql)

def drop_db(name):
    try:
        with connect(
            host="localhost",
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        ) as connection:
            create_db_query = f"DROP DATABASE IF EXISTS {name}"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)

if __name__ == '__main__':
    # create_db(db.name)
    create_tables()
    # drop_db(db.name)
    pass