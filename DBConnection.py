import psycopg2
from psycopg2 import Error
import os

class DBConnection:
    def __init__(self):
        pass

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(database = os.getenv("POSTGRES_DB", 'postgres'),
                                   user= os.getenv("POSTGRES_USER", 'postgres'),
                                   password = os.getenv("POSTGRES_PASSWORD", 'postgres'),
                                   port = 5432,
                                   host = os.getenv("POSTGRES_HOST", 'localhost'),)
            self.cursor = self.conn.cursor()
            return self.cursor
        except Error as e:
            return e

    def __exit__(self, exc_type, exc_value, exc_trace):
        if exc_value:
            if exc_value.args[0] == 'Курсор не был создан':
                print('Курсор не создан')
            elif exc_value.args[0] == 1064:
                print('Синтаксическая ошибка в запросе!')
                self.conn.commit()
                self.conn.close()
            elif exc_value.args[0] == 1146:
                print('Ошибка в запросе! Такой таблицы не существует.')
                self.conn.commit()
                self.conn.close()
            elif exc_value.args[0] == 1054:
                print('Ошибка в запросе! Такого поля не существует.')
                self.conn.commit()
                self.conn.close()
            exit(1)
        else:
            self.conn.commit()  # фиксация транзакции,изменение запроса
            self.cursor.close()
            self.conn.close()

            return True


def work_with_db(sql: str) -> list:
#для возвращения select-ответов. ответ будет представлен в виде списка словарей.
    result = []
    with DBConnection() as cursor:
        if cursor is None:
            raise ValueError('Пустой курсор')

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        for item in cursor.fetchall():
            result.append(dict(zip(schema, item)))

    return result

def make_update(sql):
#для работы с update, delete, create и тд. то есть для работы с операторами, которые ничего полезного не возвращают
    with DBConnection() as cursor:
        a = cursor.execute(sql)
    return a