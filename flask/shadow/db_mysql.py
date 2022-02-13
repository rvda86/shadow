from mysql.connector import connect, Error
from shadow import DB_USER, DB_PASSWORD
from shadow.error_handling import DatabaseError

class Database:

    create_table_users_sql =    """CREATE TABLE IF NOT EXISTS users (
                                    id CHAR(36) PRIMARY KEY,
                                    username VARCHAR(100) NOT NULL UNIQUE,
                                    email VARCHAR(100) NOT NULL UNIQUE,
                                    password VARCHAR(100) NOT NULL
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
                                    due_date DATE,
                                    completed BOOLEAN NOT NULL DEFAULT 0,                           
                                    FOREIGN KEY(user_id) REFERENCES users(id) on DELETE RESTRICT,
                                    FOREIGN KEY(topic_id) REFERENCES topics(id) on DELETE RESTRICT
                                );"""
    
    # create_table_habit_entries_sql =  """CREATE TABLE IF NOT EXISTS habit_entries (
    #                                 id TEXT PRIMARY KEY,
    #                                 user_id TEXT NOT NULL,
    #                                 topic_id TEXT NOT NULL,
    #                                 date_posted TEXT NOT NULL,
    #                                 date_edited TEXT,
    #                                 title TEXT NOT NULL,
    #                                 content TEXT,                           
    #                                 FOREIGN KEY(user) REFERENCES users(id),
    #                                 FOREIGN KEY(topic) REFERENCES topics(id) on DELETE RESTRICT
    #                             );"""

    # create_table_tags_sql =     """CREATE TABLE IF NOT EXISTS tags (
    #                                 name TEXT PRIMARY KEY,
    #                                 user INTEGER,
    #                                 FOREIGN KEY(user) REFERENCES users(id)                                
    #                             );"""
    
    create_user_sql = "INSERT INTO users (id, username, email, password) VALUES (%s, %s, %s, %s)"
    retrieve_user_by_username_sql = "SELECT * FROM users WHERE username = %s"
    retrieve_user_by_id_sql = "SELECT * FROM users WHERE id = %s"
    retrieve_all_usernames_sql = "SELECT username FROM users"
    retrieve_all_user_emails_sql = "SELECT email FROM users"
    update_user_sql = "UPDATE users SET username = %s, email = %s, password = %s where id = %s"
    delete_user_by_id_sql = "DELETE FROM users WHERE id = %s"

    create_category_sql = "INSERT INTO categories (id, user_id, name) VALUES (%s, %s, %s)"
    retrieve_category_sql = "SELECT id, name FROM categories WHERE id = %s and user_id = %s"
    retrieve_all_categories_sql = "SELECT id FROM categories WHERE user_id = %s"
    update_category_sql = "UPDATE categories SET name = %s WHERE id = %s and user_id = %s"
    delete_category_sql = "DELETE FROM categories WHERE id = %s and user_id = %s"
    delete_all_categories_user_sql = "DELETE FROM categories WHERE user_id = %s"

    create_topic_sql = "INSERT INTO topics (id, user_id, category_id, name, topic_type) VALUES (%s, %s, %s, %s, %s)"
    retrieve_topic_sql = "SELECT id, category_id, name, topic_type FROM topics WHERE id = %s and user_id = %s"
    retrieve_topic_ids_by_category_sql = "SELECT id FROM topics WHERE category_id = %s and user_id = %s"
    update_topic_sql = "UPDATE topics SET name = %s WHERE id = %s and user_id = %s"
    delete_topic_sql = "DELETE FROM topics WHERE id = %s and user_id = %s"
    delete_all_topics_user_sql = "DELETE FROM topics WHERE user_id = %s"

    create_journal_entry_sql = "INSERT INTO journal_entries (id, user_id, topic_id, date_posted, title, content) VALUES (%s, %s, %s, %s, %s, %s)"
    retrieve_journal_entry_sql = "SELECT id, topic_id, date_posted, date_edited, title, content FROM journal_entries where id = %s and user_id = %s"
    retrieve_journal_ids_by_topic_sql = "SELECT id FROM journal_entries where topic_id = %s and user_id = %s ORDER BY date_posted DESC"
    update_journal_entry_sql = "UPDATE journal_entries SET date_edited = %s, title = %s, content = %s WHERE id = %s and user_id = %s"
    delete_journal_entry_sql = "DELETE FROM journal_entries WHERE id = %s and user_id = %s"
    delete_all_journal_entries_user_sql = "DELETE FROM journal_entries WHERE user_id = %s"
   
    create_todo_entry_sql = "INSERT INTO todo_entries (id, user_id, topic_id, date_posted, task, due_date) VALUES (%s, %s, %s, %s, %s, %s)"
    retrieve_todo_entry_sql = "SELECT id, topic_id, date_posted, date_edited, task, DATE_FORMAT(due_date, '%Y-%m-%d'), completed FROM todo_entries where id = %s and user_id = %s"
    retrieve_todo_ids_by_topic_sql = "SELECT id FROM todo_entries where topic_id = %s and user_id = %s ORDER BY due_date DESC"
    update_todo_entry_sql = "UPDATE todo_entries SET date_edited = %s, task = %s, due_date = %s, completed = %s WHERE id = %s and user_id = %s"
    delete_todo_entry_sql = "DELETE FROM todo_entries WHERE id = %s and user_id = %s"
    delete_all_todo_entries_user_sql = "DELETE FROM todo_entries WHERE user_id = %s"

    delete_all_data_queries = ["SET FOREIGN_KEY_CHECKS = 0", "TRUNCATE TABLE todo_entries", "TRUNCATE TABLE journal_entries", "TRUNCATE TABLE topics", "TRUNCATE TABLE categories", "TRUNCATE TABLE users"]

    def __init__(self, name):
        self.name = name

    def create_connection(self):
        try:
            connection = connect(host="localhost", user=DB_USER, password=DB_PASSWORD, buffered=True, database=self.name)
            cursor = connection.cursor()
            return connection, cursor
        except Error as e:
            print(e)
            raise DatabaseError

    def create_table(self, sql):
        try: 
            conn, c = self.create_connection()
            c.execute(sql)
            conn.commit()
        except Error as e:
            print(e)
            raise DatabaseError
        finally:
            c.close()
            conn.close()

    def create_update_delete_record(self, sql, values):
        try:
            conn, c = self.create_connection()
            c.execute(sql, values)
            conn.commit()
        except Error as e:
            print(e)
            raise DatabaseError
        finally:
            c.close()
            conn.close()

    def retrieve_record(self, sql, values):
        try:
            conn, c = self.create_connection()
            c.execute(sql, values)
            conn.commit()
            return c.fetchone()
        except Error as e:
            print(e)
            raise DatabaseError
        finally:
            c.close()
            conn.close()

    def retrieve_all_records_by_id(self, sql, id):
        try:
            conn, c = self.create_connection()
            c.execute(sql, id)
            return c.fetchall()
        except Error as e:
            print(e)   
            raise DatabaseError 
        finally:
            c.close()
            conn.close()

    def retrieve_all_records(self, sql):
        try:
            conn, c = self.create_connection()
            c.execute(sql)
            return c.fetchall()
        except Error as e:
            print(e)
            raise DatabaseError
        finally:
            c.close()
            conn.close()

    def reset_database(self):
        try:
            conn, c = self.create_connection()
            for sql in self.delete_all_data_queries:
                c.execute(sql)
        except Error as e:
            print(e)
            raise DatabaseError
        finally:
            c.close()
            conn.close()

class DatabasePool:

    def __init__(self):
        self.instances = {"dev": Database("shadow_dev"), "testing": Database("shadow_testing")}
        self.in_use = self.instances["dev"]

    def acquire(self):
        return self.in_use

    def set_in_use(self, db_instance):
        self.in_use = self.instances[db_instance]

db_pool = DatabasePool()
db_pool.set_in_use("testing")
