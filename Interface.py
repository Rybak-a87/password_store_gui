import tkinter

from BackendJson import BackendJson
from Cipher import Cipher


class Interface:
    def __init__(self, window_name):
        self.backend = BackendJson("data")
        self.cipher = Cipher()

        self.root = tkinter.Tk()
        self.root.title(window_name)
        # self.root.iconbitmap("./ico/icon.ico")
        # размер и положение окна (середира экрана)
        wx = self.root.winfo_screenwidth()
        wy = self.root.winfo_screenheight()
        x = int(wx/2 - 600/2)
        y = int(wy/2 - 400/2)
        self.root.geometry(f"600x400+{x}+{y}")
        self.root.resizable(False, False)
        # вызов начального фрейма
        self.frame_home()

    # создание фреймa
    def create_frames(self):
        return tkinter.Frame(self.root, width=600, height=400)

    # главный экран
    def frame_home(self):
        f_home = self.create_frames()
        f_home.place(relx=0.5, rely=0.5, anchor="center")
        self.__author(f_home)

        welcome_text = "Добро пожаловать!\nДанная программа поможет вам хранить\nи управлять Вашими паролями"
        tkinter.Label(f_home, font="Arial 15", text=welcome_text).place(relx=0.5, rely=0.1, anchor="n")
        # кнопки
        buttons = ["Добавить", "Удалить", "Показать"]
        x = 80
        y = 300
        for btn in buttons:
            pressing = lambda but=btn: self.button_logics(but)
            tkinter.Button(f_home, text=btn, font="Arial 15", command=pressing,
                           ).place(x=x, y=y, width=110, height=50)
            x += 160
        # ввод ключа шифрования
        tkinter.Label(f_home, font="Arial 10", text="Ключ шифрования",
                      ).place(relx=0.05, rely=0.45, anchor="w")
        self.scrypt_key = tkinter.Entry(f_home, font="Arial 10")
        self.scrypt_key.place(relx=0.05, rely=0.5, anchor="w", width=480)
        tkinter.Button(f_home, font="Arial 7", text="Добавить ключ",
                       command=lambda but="add_key": self.button_logics(but),
                       ).place(relx=0.855, rely=0.5, anchor="w")
        self.use_scrypt_key = tkinter.Label(f_home, font="Arial 7",
                                            text="Используестя ключ по умолчанию")
        self.use_scrypt_key.place(relx=0.5, rely=0.53, anchor="n")

    # раздел добавления
    def frame_add(self):
        f_add = self.create_frames()
        f_add.place(relx=0.5, rely=0.5, anchor="center")
        self.button_back(f_add)
        self.__author(f_add)

        self.descriptions = {"Ресурс": None, "Ваш логин": None, "Ваш пароль": None}
        y = 10
        for description in self.descriptions.keys():
            tkinter.Label(f_add, font="Arial 15", text=description).place(relx=0.5, y=y, anchor="n")
            self.descriptions[description] = tkinter.Entry(f_add, font="Arial 15", width=30,
                                                           )
            self.descriptions[description].place(relx=0.5, y=y + 30, anchor="n")
            y += 100

        tkinter.Button(f_add, command=lambda but="add_data": self.button_logics(but),
                       text="Сохранить", font="Arial 16", width=20,).place(relx=0.5, rely=0.8, anchor="n")

    # раздел удаления
    def frame_del(self):
        f_del = self.create_frames()
        f_del.place(relx=0.5, rely=0.5, anchor="center")
        self.button_back(f_del)
        self.__author(f_del)

        self.temp_f_frame = f_del

        self.del_list = tkinter.Listbox(f_del, font="Arial 10", selectmode=tkinter.MULTIPLE, bd=1)
        tkinter.Button(f_del, command=lambda but="del_data": self.button_logics(but),
                       font="Arial 15", text="Удалить").place(relx=0.5, rely=0.85, anchor="n")

        # работа со списком
        self.data = self.backend.read_file()
        for atr in self.data:
            self.del_list.insert(tkinter.END, f"{self.cipher.decipher(atr)}")

        self.del_list.place(relx=0.5, y=3, anchor="n", width=444, height=330)

    # раздел просмотра
    def frame_view(self):
        f_view = self.create_frames()
        f_view.place(relx=0.5, rely=0.5, anchor="center")
        self.button_back(f_view)
        self.__author(f_view)

        self.info = tkinter.Text(f_view, font="Arial 10")

        # работа со списком
        data = self.backend.read_file()
        for k, v in data.items():
            out = f"{4*' '}{self.cipher.decipher(k)}\n" \
                  f"\tLogin: {self.cipher.decipher(v['login'])}\n" \
                  f"\tPassword: {self.cipher.decipher(v['password'])}\n" \
                  f"{110*'-'}"
            self.info.insert(tkinter.END, out)

        self.info.place(relx=0.5, y=3, anchor="n", width=446, height=380)

    # логика нажатий на кнопки
    def button_logics(self, pressing):
        if pressing == "Добавить":
            self.frame_add()
        elif pressing == "Удалить":
            self.frame_del()
        elif pressing == "Показать":
            self.frame_view()
        elif pressing == "add_data":
            self.add()
        elif pressing == "del_data":
            self.dell()
        elif pressing == "add_key":
            self.add_scrypt_key()

    # Кнопка добавить
    def add(self):
        resource = self.cipher.encipher(self.descriptions["Ресурс"].get())
        login = self.cipher.encipher(self.descriptions["Ваш логин"].get())
        password = self.cipher.encipher(self.descriptions["Ваш пароль"].get())
        if resource and login and password:
            # очистить поля
            self.descriptions["Ресурс"].delete(0, tkinter.END)
            self.descriptions["Ваш логин"].delete(0, tkinter.END)
            self.descriptions["Ваш пароль"].delete(0, tkinter.END)
            # добавление данных в память
            self.backend.add_to_file(resource, login, password)

    # кнопка удалить
    def dell(self):
        if self.data:
            need_del = [self.cipher.encipher(i) for i in self.del_list.selection_get().split("\n")]
            self.backend.del_from_file(need_del)
            # перезапуск фрейма
            self.temp_f_frame.destroy()
            self.frame_del()

    # кнопка добавить клюс шифрования
    def add_scrypt_key(self):
        key = self.scrypt_key.get()
        if key:
            self.cipher.scrypt_key_set(key.lower())
            self.use_scrypt_key["text"] = f"Используется ключ: {key}"
        else:
            self.cipher.scrypt_key_default()
            self.use_scrypt_key["text"] = "Используестя ключ по умолчанию"

    # кнопка "назад"
    def button_back(self, frame):
        tkinter.Button(frame, text="< Назад", font="Arial 8", command=lambda: frame.destroy(),
                       ).place(x=3, y=3, anchor="nw")

    # запуск окна
    def start(self):
        self.root.mainloop()

    # автор "водяной знак"
    def __author(self, root):
        my_name = "Programm by Rybak A."
        tkinter.Label(root, font="Tahoma 7", text=my_name, fg="Blue"
                      ).place(relx=1, rely=1, anchor="se")
