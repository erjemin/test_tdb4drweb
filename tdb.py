# c:/Python/2.7/python.exe
# coding=utf-8

#       ~~V<                                              2021-12-28 15:15 MSK
# ___________________Дракон_приземлился_на_поле_–_поздно_считать,_что_ты_спишь
#
import re


class TransDB:
    # db -- словарь для БД
    db = {}
    # db_replication -- если не None то в ней вложенный TransDB c транзакцией
    db_replication = None

    def cmd(self, sz_command):
        # обработчик команд
        dim_cmd = re.sub(r"\s+", " ", sz_command).split(" ")
        dim_cmd[0] = dim_cmd[0].upper()
        if len(dim_cmd) == 1:
            # команда из одного "слова" -- BEGIN, ROLLBACK, и COMMIT
            if "BEGIN" == dim_cmd[0]:
                self.begin()
            elif "ROLLBACK" == dim_cmd[0]:
                self.rollback()
            elif "COMMIT" == dim_cmd[0]:
                self.commit()
        elif len(dim_cmd) > 1:
            # команда из двух и более "слов" -- SET, GET, UNSET, COUNTS и FIND
            if "SET" == dim_cmd[0]:
                # команда типа: SET key value
                # добавляет запись {"key": "value"}
                # todo: если в value фраза разделенная пробелами то сохранится
                # todo: только первое слово! (возможно технический долг?)
                try:
                    return self.set({dim_cmd[1]: dim_cmd[2]})
                except IndexError:
                    # если нет значения ключа, запишем пустую строку
                    return self.set({dim_cmd[1]: ""})
            elif "GET" == dim_cmd[0]:
                # команда типа: GET key
                # возвращает значение "value" соответствущее "key"
                ret = self.get(dim_cmd[1])
                if ret is None:
                    print("\t\tNULL")
                else:
                    print(ret)
                return ret
            elif "UNSET" == dim_cmd[0]:
                # команда типа: UNSET key
                # удаляет запись с соответствующим "key"
                return self.unset(dim_cmd[1])
            elif "COUNTS" == dim_cmd[0]:
                # команда типа: UNSET value
                # показывает сколько разных ключей установлено для
                # запрашиваемого значения
                ret = self.counts(dim_cmd[1])
                print(ret)
                return ret
            elif "FIND" == dim_cmd[0]:
                # команда типа: FIND value
                # возвращает ключи, для которых установлено запрашиваемое
                # значение
                ret = self.find(dim_cmd[1])
                print(ret)
                return ret

    def set(self, dict_set):
        """
        SET -- сохраняет аргумент в базе данных

        :param dict_set: {ключ: значение} (-> dict)
        :return: True (-> bool)
        """
        if self.db_replication is None:
            self.db.update(dict_set)
            # print(self.db)
            return True
        else:
            return self.db_replication.set(dict_set)

    def get(self, sz_key):
        """
        GET -- Возвращает, ранее сохраненную переменную. Если такой
        переменной не было сохранено -- возвращает NULL

        :param sz_key: ключ (-> str)
        :return: значение (-> str)
        """
        if self.db_replication is None:
            # print(self.db)
            try:
                return self.db[sz_key]
            except KeyError:
                # нет значения с таким ключом или ключ не задан
                return None
        else:
            return self.db_replication.get(sz_key)

    def unset(self, sz_key):
        """
        UNSET --  удаляет, ранее установленную переменную. Если значение
        не было установлено, не делает ничего

        :param sz_key: ключ (-> str)
        :return: значение (-> str)
        """
        if self.db_replication is None:
            # print(self.db)
            return self.db.pop(sz_key, False)
        else:
            return self.db_replication.unset(sz_key)

    def counts(self, sz_value):
        """
        UNSET -- показывает сколько раз данные значение встречается
        в базе данных

        :param sz_value: значение (-> str)
        :return: число (-> int)
        """
        if self.db_replication is None:
            ret = sum(x == sz_value for x in self.db.values())
            # print(self.db)
            return ret
        else:
            return self.db_replication.counts(sz_value)

    def find(self, sz_value):
        """
        FIND -- выводит найденные установленные переменные для данного
        значения

        :param sz_value: значение (-> str)
        :return: список ключей [key1, key2, ... ] (-> list)
        """
        if self.db_replication is None:
            ret = list(x for x, y in self.db.items() if y == sz_value)
            # print(self.db)
            return ret
        else:
            return self.db_replication.find(sz_value)

    def begin(self):
        """
        BEGIN — начало транзакции

        :return: None
        """
        if self.db_replication is None:
            self.db_replication = TransDB()
            self.db_replication.db = self.db.copy()
        else:
            self.db_replication.begin()
        # print(self.db)

    def rollback(self):
        """
        ROLLBACK — откат текущей (самой внутренней) транзакции

        :return: None
        """
        if self.db_replication:
            if self.db_replication.db_replication is None:
                # во вложенной структуре нет транзакции, удаляем текущую
                self.db_replication = None
            else:
                # есть вложенная транзакции, переводим запрос в неё
                self.db_replication.rollback()
        # print(self.db)

    def commit(self):
        """
        COMMIT — фиксация изменений текущей (самой внутренней) транзакции

        :return: None
        """
        if self.db_replication:
            if self.db_replication.db_replication is None:
                self.db = self.db_replication.db.copy()
                self.db_replication = None
            else:
                self.db_replication.commit()
        # print(self.db)
