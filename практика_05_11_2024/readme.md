
# описание

## для всех скриптов

скрипты могут:

* подключиться к существующей таблице
* создать таблицу из csv файла

дальше появится интерфейс с такими возможностями:
* вывести заголовки столбцов таблицы
* добавить введённую строку
* вывести диапазон строк во всей таблице
* вывести диапазон строк в одном столбце
* вывести столбец по имени
* удалить диапазон строк
* удалить таблицу
* завершить программу.

для всех скриптов нужна библиотека pandas

подключаются все скрипты по следующему списку данных:

* имя пользователь базы данных
* пароль
* адрес базы данных в сети
* имя базы данных

если что-то меняется, скрипт об этом сообщает.

## для postgres

для postgres нужны библиотеки psycopg2 и sqlalhemy

## для mongodb

для mongodb нужна библиотека motor

## для clickhouse

нужна библиотека infi.clickhouse_orm