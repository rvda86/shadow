from mysql.connector import connect, Error
from shadow import DB_USER, DB_PASSWORD, DB_TESTING, DB_DEVELOPMENT
from shadow.error_handling import DatabaseError

class Database:

    create_user_sql = "INSERT INTO users (id, username, email, password) VALUES (%s, %s, %s, %s)"
    retrieve_user_by_username_sql = "SELECT * FROM users WHERE username = %s"
    retrieve_user_by_id_sql = "SELECT * FROM users WHERE id = %s"
    retrieve_user_by_email_sql = "SELECT * FROM users WHERE email = %s"
    retrieve_all_usernames_sql = "SELECT username FROM users"
    retrieve_all_emails_sql = "SELECT email FROM users"
    update_user_sql = "UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s"
    delete_user_by_id_sql = "DELETE FROM users WHERE id = %s"
    update_email_verification_status_sql = "UPDATE users SET email_verified = %s WHERE id = %s"
    update_password_sql = "UPDATE users SET password = %s WHERE id = %s"

    create_journal_tag_sql = "INSERT INTO journal_tags (id, user_id, tag_id, journal_id) VALUES (%s, %s, %s, %s)"
    retrieve_journal_tag_sql = "SELECT id, tag_id, journal_id FROM journal_tags WHERE id = %s and user_id = %s"
    retrieve_journal_tag_ids_by_journal_entry_sql = "SELECT tag_id FROM journal_tags WHERE journal_id = %s AND user_id = %s"
    delete_journal_tag_sql = "DELETE FROM journal_tags WHERE id = %s AND user_id = %s"

    create_tag_sql = "INSERT INTO tags (id, user_id, tag) VALUES (%s, %s, %s)"
    retrieve_tag_sql = "SELECT id, tag FROM tags WHERE id = %s AND user_id = %s"
    retrieve_tag_ids_by_user_sql = "SELECT id FROM tags WHERE user_id = %s"
    retrieve_tags_by_user_sql = "SELECT tag FROM tags WHERE user_id = %s"
    update_tag_sql = "UPDATE tags SET tag = %s WHERE id = %s AND user_id = %s"
    delete_tag_sql = "DELETE FROM tags WHERE id = %s AND user_id = %s"

    create_habit_days_completed_sql = "INSERT INTO habit_days_completed (user_id, habit_id, day) VALUES (%s, %s, %s)"
    retrieve_habit_days_completed_sql = "SELECT day FROM habit_days_completed WHERE habit_id = %s AND user_id = %s"
    delete_habit_days_completed_sql = "DELETE FROM habit_days_completed WHERE habit_id = %s AND user_id = %s AND day = %s"

    create_habit_entry_sql = "INSERT INTO habit_entries (id, user_id, topic_id, date_posted, name) VALUES (%s, %s, %s, %s, %s)"
    retrieve_habit_entry_sql = "SELECT id, topic_id, date_posted, date_edited, name FROM habit_entries WHERE id = %s AND user_id = %s"
    retrieve_habit_ids_by_topic_sql = "SELECT id FROM habit_entries WHERE topic_id = %s AND user_id = %s ORDER BY date_posted DESC"
    update_habit_entry_sql = "UPDATE habit_entries SET date_edited = %s, name = %s WHERE id = %s AND user_id = %s"
    delete_habit_entry_sql = "DELETE FROM habit_entries WHERE id = %s AND user_id = %s"
    delete_all_habit_entries_user_sql = "DELETE FROM habit_entries WHERE user_id = %s"

    create_category_sql = "INSERT INTO categories (id, user_id, name) VALUES (%s, %s, %s)"
    retrieve_category_sql = "SELECT id, name FROM categories WHERE id = %s AND user_id = %s"
    retrieve_all_categories_sql = "SELECT id FROM categories WHERE user_id = %s"
    update_category_sql = "UPDATE categories SET name = %s WHERE id = %s AND user_id = %s"
    delete_category_sql = "DELETE FROM categories WHERE id = %s AND user_id = %s"
    delete_all_categories_user_sql = "DELETE FROM categories WHERE user_id = %s"

    create_topic_sql = "INSERT INTO topics (id, user_id, category_id, name, topic_type) VALUES (%s, %s, %s, %s, %s)"
    retrieve_topic_sql = "SELECT id, category_id, name, topic_type FROM topics WHERE id = %s AND user_id = %s"
    retrieve_topic_ids_by_category_sql = "SELECT id FROM topics WHERE category_id = %s AND user_id = %s"
    update_topic_sql = "UPDATE topics SET name = %s WHERE id = %s AND user_id = %s"
    delete_topic_sql = "DELETE FROM topics WHERE id = %s AND user_id = %s"
    delete_all_topics_user_sql = "DELETE FROM topics WHERE user_id = %s"

    create_journal_entry_sql = "INSERT INTO journal_entries (id, user_id, topic_id, date_posted, title, content) VALUES (%s, %s, %s, %s, %s, %s)"
    retrieve_journal_entry_sql = "SELECT id, topic_id, date_posted, date_edited, title, content FROM journal_entries WHERE id = %s AND user_id = %s"
    retrieve_journal_ids_by_topic_sql = "SELECT id FROM journal_entries WHERE topic_id = %s AND user_id = %s ORDER BY date_posted DESC"
    update_journal_entry_sql = "UPDATE journal_entries SET date_edited = %s, title = %s, content = %s WHERE id = %s AND user_id = %s"
    delete_journal_entry_sql = "DELETE FROM journal_entries WHERE id = %s AND user_id = %s"
    delete_all_journal_entries_user_sql = "DELETE FROM journal_entries WHERE user_id = %s"
   
    create_todo_entry_sql = "INSERT INTO todo_entries (id, user_id, topic_id, date_posted, task) VALUES (%s, %s, %s, %s, %s)"
    retrieve_todo_entry_sql = "SELECT id, topic_id, date_posted, date_edited, task, completed FROM todo_entries WHERE id = %s AND user_id = %s"
    retrieve_todo_ids_by_topic_sql = "SELECT id FROM todo_entries WHERE topic_id = %s AND user_id = %s ORDER BY date_posted DESC"
    update_todo_entry_sql = "UPDATE todo_entries SET date_edited = %s, task = %s, completed = %s WHERE id = %s AND user_id = %s"
    delete_todo_entry_sql = "DELETE FROM todo_entries WHERE id = %s AND user_id = %s"
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

    def create_update_delete(self, sql, values):
        try:
            conn, c = self.create_connection()
            conn.autocommit = False
            if isinstance(sql, list):
                for query in sql:
                    c.execute(query, values)
            else:
                c.execute(sql, values)
            conn.commit()
        except Error as e:
            print(e)
            conn.rollback()
            raise DatabaseError
        finally:
            c.close()
            conn.close()

    def retrieve(self, sql, values):
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

    def retrieve_all_by_id(self, sql, id):
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

    def retrieve_all(self, sql):
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
        self.instances = {"development": Database(DB_DEVELOPMENT), "testing": Database(DB_TESTING)}
        self.in_use = self.instances["development"]

    def acquire(self):
        return self.in_use

    def set_in_use(self, db_instance):
        self.in_use = self.instances[db_instance]

db_pool = DatabasePool()
db_pool.set_in_use("development")
