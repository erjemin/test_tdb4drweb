# c:/Python/2.7/python.exe
# coding=utf-8

#       ~~V<                                              2021-12-31 14:10 MSK
# ___________________Дракон_приземлился_на_поле_–_поздно_считать,_что_ты_спишь
#
import sys
from tdb import TransDB


if __name__ == '__main__':
    # инициализируем БД t_db (база ключей с транзакциями)
    t_db = TransDB()

    # ----------- Читаем дамп предыдущей сессии (если он задан)
    # считываем аргумент командной строки (имя файла дампа)
    if len(sys.argv) > 1:
        # если аргумент есть, то загружаем дамп предыдущей сессии
        file_name = sys.argv[1]
        # print(file_name)
        try:
            # читаем файл дампа (если он есть)
            with open(file_name, "r") as file_dump:
                while True:
                    sz_command = file_dump.readline()
                    if not sz_command:
                        # файл дампа кончился, перестаем читать дамп
                        # и закрываем файл
                        break
                    # отправляем команду дампа в обработчик
                    t_db.cmd(sz_command.strip())
        except IOError:
            # не удалось прочитать дамп (ещё не создан или занят)
            pass
    else:
        file_name = "tdb_dump_default.data"
    sz_command = ""
    # узнаём версию Python, в которой работаем
    i_py_ver = int(sys.version[0])

    # ----------- Получаем ввод команд
    while "END" != sz_command.upper().strip():
        if i_py_ver == 2:       # для Python 2.x
            sz_command = str(raw_input())
        else:                   # для Python 3.x
            sz_command = str(input())
        t_db.cmd(sz_command.lstrip())

    # ----------- Записываем завершающий дамп состояния
    try:
        with open(file_name, "w") as file_dump:
            for dict_i in t_db.db:
                file_dump.write("SET %s %s\n" % (dict_i, t_db.db[dict_i]))
    except IOError:
        # не удалось открыть файл и записать дамп (файл занят?)
        pass
