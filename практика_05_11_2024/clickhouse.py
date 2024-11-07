import csv
from datetime import date
from infi.clickhouse_orm import Database, Model, DateField, StringField, Int32Field, engines

class BaseModel(Model):
    id = Int32Field()
    date = DateField()

def get_user_input(prompt):
    return input(prompt)

def connect_to_database():
    user = get_user_input("Введите имя пользователя базы данных: ")
    host = get_user_input("Введите адрес хоста базы данных: ")
    password = get_user_input("Введите пароль пользователя базы данных или оставьте пустым: ")

    db_name = get_user_input("Введите имя базы данных: ")
    try:
        db = Database(db_name, db_url=f'http://{user}:{password}@{host}')
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

    return db

def get_model_cls_from_table(db, table_name):
    query = f"DESCRIBE TABLE {table_name}"
    try:
        description = db.select(query)
        fields = {'id': Int32Field(), 'date': DateField()}
        for column in description:
            column_name = column.name
            column_type = column.type
            if column_name not in fields:
                if "String" in column_type:
                    fields[column_name] = StringField()
                elif "Date" in column_type:
                    fields[column_name] = DateField()

        model_cls = type(table_name.capitalize(), (BaseModel,), fields)
        return model_cls

    except Exception as e:
        print(f"Ошибка получения структуры таблицы: {e}")
        return None

def create_table_from_csv(db, file_path):
    table_name = file_path.split('/')[-1].split('.')[0]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)

            fields = {'id': Int32Field(), 'date': DateField()}
            fields.update({header: StringField() for header in headers})

            fields['engine'] = engines.MergeTree(
                date_col='date',
                order_by=['id'],
            )

            model_cls = type(table_name.capitalize(), (BaseModel,), fields)
            db.create_table(model_cls)

            buffer = []
            chunk_size = 1000000
            today = date.today()

            for idx, row in enumerate(reader):
                row_data = {headers[i]: value for i, value in enumerate(row)}
                row_data['id'] = idx
                row_data['date'] = today
                record = model_cls(**row_data)
                buffer.append(record)

                if len(buffer) >= chunk_size:
                    db.insert(buffer)
                    buffer.clear()

            if buffer:
                db.insert(buffer)

        print(f"Таблица '{table_name}' успешно создана и заполнена данными.")
        return model_cls

    except Exception as e:
        print(f"Ошибка при создании таблицы из CSV: {e}")
        return None

def show_columns(model_cls):
    print("Заголовки столбцов:", "\t".join(field_name for field_name in model_cls.fields()))

def insert_row_to_table(db, model_cls, table_name, row_input):
    values = row_input.split()
    fields = list(model_cls.fields().keys())  # Получаем имена полей модели

    try:
        # Получение текущего максимального ID
        current_max_id_query = f'SELECT MAX(id) AS max_id FROM {table_name}'
        current_max_id_result = db.raw(current_max_id_query)

        # Обработка результата запроса и расчет нового ID
        current_max_id = current_max_id_result[0]['max_id'] if current_max_id_result and 'max_id' in current_max_id_result[0] else -1
        new_id = current_max_id + 1

        # Данные для вставки
        row_data = {'id': new_id, 'date': date.today()}

        # Проверяем длину значений и добавляем их в row_data соответственно
        if len(values) != len(fields) - 2:  # Без учета 'id' и 'date'
            print(f"Количество значений не совпадает с количеством столбцов. Ожидается {len(fields) - 2}, получено {len(values)}.")
            return

        # Обновляем срезом по существующим полям
        row_data.update({field_name: value for field_name, value in zip(fields[2:], values)})

        # Отладочная информация
        print(f"Для вставки данные: {row_data}")

        # Создание и вставка записи
        record = model_cls(**row_data)
        db.insert([record])
        print("Строка добавлена.")
    except Exception as e:
        print(f"Ошибка добавления строки: {e}")

def display_rows(rows, model_cls):
    headers = list(model_cls.fields())
    print("\t".join(headers))
    for row in rows:
        values = [getattr(row, header) for header in headers]
        print("\t".join(map(str, values)))

def main():
    db = connect_to_database()
    if db is None:
        return

    choice = get_user_input("Введите 1 для работы с существующей таблицей, 2 для загрузки из CSV: ")

    model_cls = None
    table_name = ""
    if choice == '1':
        table_name = get_user_input("Введите имя таблицы: ")
        model_cls = get_model_cls_from_table(db, table_name)
        if model_cls is None:
            return
    elif choice == '2':
        file_path = get_user_input("Введите путь к файлу CSV: ")
        model_cls = create_table_from_csv(db, file_path)
        if model_cls is None:
            return
        table_name = model_cls.table_name()

    while True:
        action = get_user_input(
            "\nВыберите действие:\n"
            "1: Вывести заголовки столбцов\n"
            "2: Добавить строки\n"
            "3: Вывести строки с/по номеру\n"
            "4: Вывести строки с/по номеру в столбце\n"
            "5: Вывести столбец по имени\n"
            "6: Удалить таблицу\n"
            "7: Удалить строки с/по номеру\n"
            "8: Выйти\n"
        )

        if action == '1':
            show_columns(model_cls)

        elif action == '2':
            row_input = get_user_input("Введите строку для добавления (значения через пробел): ")
            insert_row_to_table(db, model_cls, table_name, row_input)

        elif action == '3':
            start = int(get_user_input("Введите начальный номер строки: "))
            end = int(get_user_input("Введите конечный номер строки: "))
            try:
                query = f'SELECT * FROM {table_name} LIMIT {end-start+1} OFFSET {start}'
                rows = db.select(query, model_cls)
                display_rows(rows, model_cls)
            except Exception as e:
                print(f"Ошибка вывода строк: {e}")

        elif action == '4':
            start = int(get_user_input("Введите начальный номер строки: "))
            end = int(get_user_input("Введите конечный номер строки: "))
            column = get_user_input("Введите имя столбца для вывода: ")
            try:
                query = f'SELECT {column} FROM {table_name} LIMIT {end-start+1} OFFSET {start}'
                rows = db.select(query)
                for row in rows:
                    print(getattr(row, column))
            except Exception as e:
                print(f"Ошибка вывода строк в столбце: {e}")

        elif action == '5':
            column = get_user_input("Введите имя столбца: ")
            try:
                query = f'SELECT {column} FROM {table_name}'
                rows = db.select(query)
                for row in rows:
                    print(getattr(row, column))
            except Exception as e:
                print(f"Ошибка вывода столбца: {e}")

        elif action == '6':
            try:
                db.drop_table(model_cls)
                print(f"Таблица '{table_name}' была удалена.")
                break
            except Exception as e:
                print(f"Ошибка удаления таблицы: {e}")

        elif action == '7':
            start = int(get_user_input("Введите начальный номер строки для удаления: "))
            end = int(get_user_input("Введите конечный номер строки для удаления: "))
            try:
                db.raw(f'ALTER TABLE {table_name} DELETE WHERE id >= {start} AND id <= {end}')
                print(f"Строки с {start} по {end} были удалены.")
            except Exception as e:
                print(f"Ошибка удаления строк: {e}")

        elif action == '8':
            break

        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == '__main__':
    main()
