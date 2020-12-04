class Cipher:
    def __init__(self):
        self.scrypt_key_default()

    # ключ шифра по умолчанию
    def scrypt_key_default(self):
        self.__scrypt_key = "abcdefghijklmnopqrstuvwxyz0123456789"
        self.__sorted_scrypt_key(self.__scrypt_key)

    # обновисть ключ шифра
    def scrypt_key_set(self, key):
        self.__scrypt_key = key
        self.__sorted_scrypt_key(self.__scrypt_key)

    # сортировка ключа шифрования и удаление повторяющихся символов
    def __sorted_scrypt_key(self, scrypt_key):
        check_list = []
        self.__scrypt_key_letters = ""
        self.__scrypt_key_numbers = ""
        for i in scrypt_key:
            if i not in check_list:
                if i.isalpha():
                    self.__scrypt_key_letters += i
                else:
                    self.__scrypt_key_numbers += i
                check_list.append(i)

    # зашифровать
    def encipher(self, text):
        result = ""
        shift = len(text) + 7
        for i in text:
            if i.lower() in self.__scrypt_key_letters:
                result += self.__shift_to_right(i, self.__scrypt_key_letters, shift)
            elif i in self.__scrypt_key_numbers:
                result += self.__shift_to_right(i, self.__scrypt_key_numbers, shift)
            else:
                result += i
        return result

    # разшифровать
    def decipher(self, text):
        result = ""
        shift = len(text) + 7
        for i in text:
            if i.lower() in self.__scrypt_key_letters:
                result += self.__shift_to_left(i, self.__scrypt_key_letters, shift)
            elif i in self.__scrypt_key_numbers:
                result += self.__shift_to_left(i, self.__scrypt_key_numbers, shift)
            else:
                result += i
        return result

    # сдвиг вправо
    @staticmethod
    def __shift_to_right(letter, string, n):
        new_index = string.index(letter.lower()) + n
        while new_index >= len(string):
            new_index -= len(string)
        if letter.isupper():
            result = string[new_index].upper()
        else:
            result = string[new_index]

        return result

    # сдвиг в лево
    @staticmethod
    def __shift_to_left(letter, string, n):
        new_index = string.index(letter.lower()) - n
        while new_index < 0:
            new_index += len(string)
        if letter.isupper():
            result = string[new_index].upper()
        else:
            result = string[new_index]
        return result

