import sqlite3 as sq


class Answer:
    def __init__(self, file):
        self.open = open(file, "r", encoding='UTF-8')

    def get_string(self, n):
        l = self.open.read().split("\n")
        self.open.seek(0)
        if n <= len(l):
            return l[n]
        else:
            print("No such string number")


class Database:

    def __init__(self, database):
        self.conection = sq.connect(database)
        self.cursor = self.conection.cursor()

    def new_user(self, user):
        with self.conection:
            return self.cursor.execute("INSERT INTO users (id, name, tel, status) VALUES (?,?,?,?)",
                                       (user, None, None, 0))

    def new_admin(self, admin):
        with self.conection:
            return self.cursor.execute("INSERT INTO users (id, status) VALUES (?,?)", (admin, 0))

    def get_contact(self, contact):
        id = contact['user_id']
        name = contact["first_name"]
        tel = contact["phone_number"]
        with self.conection:
            return self.cursor.execute("UPDATE users SET tel = ?, name = ? WHERE id = ?", (tel, name, id,))

    def check_user(self, id):
        with self.conection:
            a = self.cursor.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchall()
            if len(a) > 0:
                return True
            else:
                return False

    def start_chat(self, user):
        with self.conection:
            return self.cursor.execute("UPDATE users SET status = 1 WHERE id = ?", (user,))

    def finish_chat(self, user):
        with self.conection:
            return self.cursor.execute("UPDATE users SET status = 0 WHERE id = ?", (user,))

    def admin_list(self):
        with self.conection:
            return self.cursor.execute("SELECT id FROM admins WHERE status = 0").fetchall()

    def set_admin(self, user, admin):
        with self.conection:
            return self.cursor.execute("UPDATE admins SET status = ? WHERE id = ?", (user, admin,)) and self.cursor.execute("UPDATE users SET status = ? WHERE id = ?", (admin, user))

    def check_status(self, user):
        with self.conection:
            return self.cursor.execute("SELECT status FROM users WHERE id = ?", (user,)).fetchall()[0][0]

    def is_admin(self, user):
        with self.conection:
            a = self.cursor.execute("SELECT * FROM admins WHERE id = ?", (user,)).fetchall()
            if len(a) > 0:
                return True
            else:
                return False
    def free_admin(self, admin):
        with self.conection:
            return self.cursor.execute("UPDATE admins SET status = 0 WHERE id = ?", (admin,))

    def close(self):
        self.conection.close()