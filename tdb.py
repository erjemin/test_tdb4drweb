# c:/Python/2.7/python.exe
# coding=utf-8

#       ~~V<                                              2021-12-28 15:15 MSK
# ___________________Дракон_приземлился_на_поле_–_поздно_считать,_что_ты_спишь
#
import sys
import re


class TransDB:
    db = {}

    def __init__(self):
        self.db = {}

    # @staticmethod
    def cmd(self, sz_command):
        # обработчик команд
        sz_command = re.sub(r"\s+", " ", sz_command.upper())
        # print(sz_command)
        dim_cmd = sz_command.split(" ")
        if "SET" == dim_cmd[0] and len(dim_cmd) > 1:
            # команда типа: SET key value
            # она добавляет запись {"key": "value"} в базу (если key определён)
            try:
                ret = self.set({dim_cmd[1]: dim_cmd[2]})
                # print(self.db)
                return ret
            except IndexError:
                # если нет значения ключа, запишем пустую строку
                ret = self.set({dim_cmd[1]: ""})
                # print(self.db)
                return False
        elif "GET" == dim_cmd[0] and len(dim_cmd) > 1:
            # команда типа: GET key
            # она возвращает значение "value" соответствущее "key"
            ret = self.get(dim_cmd[1])
            # print(self.db)
            return ret
        elif "UNSET" == dim_cmd[0] and len(dim_cmd) > 1:
            # команда типа: UNSET key
            # удаляет запись с соответствующим "key"
            ret = self.unset(dim_cmd[1])
            # print(self.db)
            return ret
        elif "COUNTS" == dim_cmd[0] and len(dim_cmd) > 1:
            # команда типа: UNSET value
            # показывает сколько разных ключей установлено для
            # запрашиваемого значения
            ret = self.counts(dim_cmd[1])
            # print(self.db)
            return ret
        elif "FIND" == dim_cmd[0] and len(dim_cmd) > 1:
            # команда типа: FIND value
            # возвращает ключи, для которых установлено запрашиваемое
            # значение
            ret = self.find(dim_cmd[1])
            # print(self.db)
            return ret

    def set(self, dict_set):
        """
        SET -- сохраняет аргумент в базе данных

        :param dict_set: {ключ: значение} (-> dict)
        :return: True (-> bool)
        """
        self.db.update(dict_set)
        return True

    def get(self, sz_key):
        """
        GET -- Возвращает, ранее сохраненную переменную. Если такой
        переменной не было сохранено -- возвращает NULL

        :param sz_key: ключ (-> str)
        :return: значение (-> str)
        """
        try:
            print(self.db[sz_key])
            return self.db[sz_key]
        except KeyError:
            # нет значения с таким ключом или ключ не задан
            print("\t\tNULL")
            return None

    def unset(self, sz_key):
        """
        UNSET --  удаляет, ранее установленную переменную. Если значение
        не было установлено, не делает ничего

        :param sz_key: ключ (-> str)
        :return: значение (-> str)
        """
        return self.db.pop(sz_key, False)

    def counts(self, sz_value):
        """
        UNSET -- показывает сколько раз данные значение встречается
        в базе данных

        :param sz_value: значение (-> str)
        :return: число (-> int)
        """
        ret = sum(x == sz_value for x in self.db.values())
        print(ret)
        return ret

    def find(self, sz_value):
        """
        FIND -- выводит найденные установленные переменные для данного
        значения

        :param sz_value: значение (-> str)
        :return: список ключей [key1, key2, ... ] (-> list)
        """
        ret = list(x for x, y in self.db.items() if y == sz_value)
        print(ret)
        return ret

