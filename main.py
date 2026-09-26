import sqlite3
import hashlib

DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            sex TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register(username, password, sex):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, sex) VALUES (?, ?, ?)",
            (username, hash_password(password), sex)
        )
        conn.commit()
        return True, f"Пользователь '{username}' успешно зарегистрирован."
    except sqlite3.IntegrityError:
        return False, f"Имя '{username}' уже занято, выбери другое."
    finally:
        conn.close()


def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False, "Введён неверный логин."
    if hash_password(password) == row[0]:
        return True, f"Добро пожаловать, {username}!"
    return False, "Неверный пароль."

def show_user():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, sex FROM users")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("Пользователей пока нет.")
    for row in rows:
        print(f"{row[0]} - {row[1]}")

def delete_info_from_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")
        conn.commit()
        print("Таблица users успешно полностью очищена, счетчик ID сброшен.")
    except Exception as e:
        conn.rollback()  
        print(f"Произошла ошибка при очистке: {e}")
        raise e
    finally:
        conn.close() 

def delete_db():
        while True:
            ans = input("Вы уверены? y/n: ").strip().lower()
            if ans == "y":
                print("Удаление данных")
                delete_info_from_db()
                break
            elif ans == "n":
                print("Отмена действия")
                break
            else:
                print("Введите y или n.")

if __name__ == "__main__":
    # Этот блок сработает, только если запустить файл напрямую:
    #   python database.py
    # При импорте (from database import ...) он НЕ выполняется —
    # удобно для быстрого теста бэкенда без GUI.
    create_table()
    ok, msg = register("test_user", "1234", "Male")
    print(msg)