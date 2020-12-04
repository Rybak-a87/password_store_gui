import json


class BackendJson:
    def __init__(self, file_name):
        self.file_name = f"data/{file_name}.json"
        self.create_file(self.file_name)

    # создать файл
    def create_file(self, file_name):
        try:
            file = open(file_name, "r", encoding="utf-8")
        except FileNotFoundError:
            file = open(file_name, "w", encoding="utf-8")
            json.dump({}, file, indent=4)
        file.close()

    # файл в cловарь
    def read_file(self):
        with open(self.file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    # добавить в файл
    def add_to_file(self, resource, login, password):
        added = {}
        added[resource] = {}
        added[resource]["login"] = login
        added[resource]["password"] = password
        temp_data = self.read_file() | added    # for python >= 3.9
        # temp_data = self.read_file()    # for python < 3.9
        # temp_data.update(added)         # for python < 3.9
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(temp_data, f, indent=4)

    # удалить с файла
    def del_from_file(self, need_del):
        temp_data = self.read_file()
        for i in need_del:
            temp_data.pop(i)
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(temp_data, f, indent=4)

