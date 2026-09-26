import tkinter as tk
from tkinter import messagebox, ttk
import threading

from main import create_table, register, login, show_user, delete_db


def on_register():
    username = entry_login_reg.get().strip()
    password = entry_password_reg.get().strip()
    sex = sex_var.get()

    if not username or not password or not sex:
        messagebox.showwarning("Ошибка", "Заполни логин, пароль и выбери пол.")
        return

    ok, message = register(username, password, sex)
    if ok:
        messagebox.showinfo("Регистрация", message)
    else:
        messagebox.showerror("Регистрация", message)


def on_login():
    username = entry_login_login.get().strip()
    password = entry_password_login.get().strip()

    ok, message = login(username, password)
    if ok:
        messagebox.showinfo("Вход", message)
    else:
        messagebox.showerror("Вход", message)


def show_login_screen():
    register_frame.grid_remove()
    login_frame.grid()


def show_register_screen():
    login_frame.grid_remove()
    register_frame.grid()


create_table()

root = tk.Tk()
root.title("App")
root.geometry("500x500")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# ---------- Форма регистрации ----------
register_frame = ttk.Frame(root)
register_frame.grid(row=0, column=0)

ttk.Label(register_frame, text="Welcome!").grid(row=0, column=0, pady=(20, 12))

ttk.Label(register_frame, text="Login").grid(row=1, column=0, pady=(0, 4))
entry_login_reg = ttk.Entry(register_frame)
entry_login_reg.grid(row=2, column=0, padx=12, pady=(0, 12))

ttk.Label(register_frame, text="Password").grid(row=3, column=0, pady=(0, 4))
entry_password_reg = ttk.Entry(register_frame, show="*")
entry_password_reg.grid(row=4, column=0, padx=12, pady=(0, 12))

sex_var = tk.StringVar(value="")
ttk.Radiobutton(register_frame, text="Male", variable=sex_var, value="Male").grid(row=5, column=0)
ttk.Radiobutton(register_frame, text="Female", variable=sex_var, value="Female").grid(row=6, column=0)

ttk.Button(register_frame, text="Register", width=25, command=on_register).grid(row=7, column=0, pady=(16, 4))
ttk.Button(register_frame, text="Уже есть аккаунт? Войти", width=25, command=show_login_screen).grid(row=8, column=0, pady=(4, 4))
ttk.Button(register_frame, text="Выход", width=25, command=root.destroy).grid(row=9, column=0, pady=(4, 20))

# ---------- Форма входа ----------
login_frame = ttk.Frame(root)
login_frame.grid(row=0, column=0)

ttk.Label(login_frame, text="Welcome back!").grid(row=0, column=0, pady=(20, 12))

ttk.Label(login_frame, text="Login").grid(row=1, column=0, pady=(0, 4))
entry_login_login = ttk.Entry(login_frame)
entry_login_login.grid(row=2, column=0, padx=12, pady=(0, 12))

ttk.Label(login_frame, text="Password").grid(row=3, column=0, pady=(0, 4))
entry_password_login = ttk.Entry(login_frame, show="*")
entry_password_login.grid(row=4, column=0, padx=12, pady=(0, 12))

ttk.Button(login_frame, text="Login", width=25, command=on_login).grid(row=5, column=0, pady=(16, 4))
ttk.Button(login_frame, text="Нет аккаунта? Зарегистрироваться", width=25, command=show_register_screen).grid(row=6, column=0, pady=(4, 4))
ttk.Button(login_frame, text="Quit", width=25, command=root.destroy).grid(row=7, column=0, pady=(4, 20))

login_frame.grid_remove()  # по умолчанию показываем регистрацию


def console_menu():
    while True:
        choice = input("1- Показать юзеров\n2- Удалить всю базу данных\n3- Выход\n").strip()
        if choice == "1":
            show_user()
        elif choice == "2":
            delete_db()
        elif choice == "3":
            print("Завершение работы программы")
            root.after(0, root.destroy)
            break
        else:
            print("Такого нет...")


threading.Thread(target=console_menu, daemon=True).start()
root.mainloop()