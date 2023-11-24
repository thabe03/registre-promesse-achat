import sqlite3
import os

class Favorite:
    def __init__(self, idPost, idUser, idUserOwner):
        self.idPost = idPost
        self.idUser = idUser
        self.idUserOwner = idUserOwner

    @staticmethod
    def init_database():
        conn = sqlite3.connect('favorite.db')
        cursor = conn.cursor()
        def is_file_empty(file_path):
            return os.path.exists(file_path) and os.stat(file_path).st_size == 0

        empty = is_file_empty('favorite.db')
        if empty:
            try:
                cursor.execute('''
                    CREATE TABLE favorites (
                        id INTEGER PRIMARY KEY,
                        idPost INTEGER NOT NULL,
                        idUser INTEGER NOT NULL,
                        idUserOwner INTEGER NOT NULL,
                        FOREIGN KEY (idPost) REFERENCES posts (id),
                        FOREIGN KEY (idUser) REFERENCES users (id),
                        FOREIGN KEY (idUserOwner) REFERENCES users (id)
                    )
                ''')
                conn.commit()
            except Exception as e:
                print(e)
        else:
            print("Database already exists.")

        conn.close()
    
    def save(self):
        conn = sqlite3.connect('favorite.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO favorites (idPost, idUser, idUserOwner) VALUES (?, ?, ?)',
                (self.idPost, self.idUser, self.idUserOwner)
            )
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('favorite.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM favorites')
            rows = cursor.fetchall()

            favorites = []
            for row in rows:
                favorite = Favorite(row[1], row[2], row[3])
                favorites.append(favorite)

            return favorites
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = sqlite3.connect('favorite.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM favorites WHERE idUser = ?', (user_id,))
            rows = cursor.fetchall()

            favorites = []
            for row in rows:
                favorite = Favorite(row[1], row[2], row[3])
                favorites.append(favorite)

            return favorites
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def delete(self):
        conn = sqlite3.connect('favorite.db')
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM favorites WHERE idPost = ? AND idUser = ? AND idUserOwner = ?', (self.idPost, self.idUser, self.idUserOwner))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_by_idPost_AND_idUserOwner(idPost, idUserOwner):
        conn = sqlite3.connect('favorite.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                'SELECT * FROM favorites WHERE idPost = ? AND idUserOwner = ?',
                (idPost, idUserOwner)
            )
            row = cursor.fetchone()

            if row:
                favorite = Favorite(row[1], row[2], row[3])
                return favorite
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_by_userOwner(idUserOwner):
        conn = sqlite3.connect('favorite.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM favorites WHERE idUserOwner = ?', (idUserOwner,))
            rows = cursor.fetchall()

            favorites = []
            for row in rows:
                favorite = Favorite(row[1], row[2], row[3])
                favorites.append(favorite)

            return favorites
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_by_idPost(idPost):
        conn = sqlite3.connect('favorite.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM favorites WHERE idPost = ?', (idPost,))
            rows = cursor.fetchall()

            favorites = []
            for row in rows:
                favorite = Favorite(row[1], row[2], row[3])
                favorites.append(favorite)

            return favorites
        except Exception as e:
            print(e)
        finally:
            conn.close()
