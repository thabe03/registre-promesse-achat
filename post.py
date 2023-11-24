import sqlite3
import os

class Post:
    def __init__(self, idUser, adresse, prixPa, prixAsk, description):
        self.idUser = idUser
        self.adresse = adresse
        self.prixPa = prixPa
        self.prixAsk = prixAsk
        self.description = description

    @staticmethod
    def init_database():
        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        def is_file_empty(file_path):
            return os.path.exists(file_path) and os.stat(file_path).st_size == 0

        empty = is_file_empty('post.db')
        if empty:
            try:
                cursor.execute('''
                    CREATE TABLE posts (
                        id INTEGER PRIMARY KEY,
                        idUser INTEGER NOT NULL,
                        adresse VARCHAR(100) NOT NULL,
                        prixPa FLOAT NOT NULL,
                        prixAsk FLOAT NOT NULL,
                        description TEXT,
                        FOREIGN KEY (idUser) REFERENCES users (id)
                    )
                ''')
                conn.commit()
            except Exception as e:
                print(e)
        else:
            print("Database already exists.")

        conn.close()

    def save(self):
        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO posts (idUser, adresse, prixPa, prixAsk, description) VALUES (?, ?, ?, ?, ?)',
                (self.idUser, self.adresse, self.prixPa, self.prixAsk, self.description)
            )
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM posts')
            rows = cursor.fetchall()

            posts = []
            for row in rows:
                post = Post(row[1], row[2], row[3], row[4], row[5])
                posts.append(post)

            return posts
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_by_adresse(adresse):
        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM posts WHERE adresse = ?', (adresse,))
            row = cursor.fetchone()

            if row:
                post = Post(row[1], row[2], row[3], row[4], row[5])
                return post
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_by_idUser(idUser):
        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM posts WHERE idUser = ?', (idUser,))
            rows = cursor.fetchall()

            posts = []
            for row in rows:
                post = Post(row[1], row[2], row[3], row[4], row[5])
                posts.append(post)

            return posts
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM posts WHERE id = ?', (id,))
            row = cursor.fetchone()

            if row:
                post = Post(row[1], row[2], row[3], row[4], row[5])
                return post
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def update(self):
        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                'UPDATE posts SET idUser = ?, prixPa = ?, prixAsk = ?, description = ? WHERE adresse = ?',
                (self.idUser, self.prixPa, self.prixAsk, self.description, self.adresse)
            )
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def delete(self):
        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM posts WHERE adresse = ?', (self.adresse,))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def getId(self):
        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM posts WHERE adresse = ?", (self.adresse,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            conn.close()
