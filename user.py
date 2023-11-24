import sqlite3
import os

class User:
    def __init__(self, firstName, lastName, email, phone, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phone = phone
        self.password = password

    @staticmethod
    def init_database():
        conn = sqlite3.connect('user.db', check_same_thread=False)
        cursor = conn.cursor()
        def is_file_empty(file_path):
            return os.path.exists(file_path) and os.stat(file_path).st_size == 0

        empty = is_file_empty('user.db')
        if empty:
            try:
                cursor.execute('''
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY,
                        firstName VARCHAR(50) NOT NULL,
                        lastName VARCHAR(50) NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        phone VARCHAR(20) NOT NULL,
                        password VARCHAR(100) NOT NULL
                    )
                ''')
                conn.commit()
            except Exception as e:
                print(e)
        else:
            print("Database already exists.")

        conn.close()

    def save(self):
        conn = sqlite3.connect('user.db', check_same_thread=False)
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (firstName, lastName, email, phone, password) VALUES (?, ?, ?, ?, ?)',
                (self.firstName, self.lastName, self.email, self.phone, self.password)
            )
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('user.db', check_same_thread=False)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM users')
            rows = cursor.fetchall()

            users = []
            for row in rows:
                user = User(row[1], row[2], row[3], row[4], row[5])
                users.append(user)

            return users
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_by_email(email):
        conn = sqlite3.connect('user.db', check_same_thread=False)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()

            if row:
                user = User(row[1], row[2], row[3], row[4], row[5])
                return user
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_by_phone(phone):
        conn = sqlite3.connect('user.db', check_same_thread=False)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM users WHERE phone = ?', (phone,))
            row = cursor.fetchone()

            if row:
                user = User(row[1], row[2], row[3], row[4], row[5])
                return user
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('user.db', check_same_thread=False)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
            row = cursor.fetchone()

            if row:
                user = User(row[1], row[2], row[3], row[4], row[5])
                return user
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def update(self):
        conn = sqlite3.connect('user.db', check_same_thread=False)
        cursor = conn.cursor()
        try:
            cursor.execute(
                'UPDATE users SET firstName = ?, lastName = ?, phone = ?, password = ? WHERE email = ?',
                (self.firstName, self.lastName, self.phone, self.password, self.email)
            )
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def delete(self):
        conn = sqlite3.connect('user.db', check_same_thread=False)
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM users WHERE phone = ?', (self.phone,))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def getId(self):
        conn = sqlite3.connect('user.db', check_same_thread=False)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM users WHERE phone = ?", (self.phone,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            conn.close()
