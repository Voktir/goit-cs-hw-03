from decor import db_connection


@db_connection
def create_db(cur, conn):
        
    # Читаємо файл з SQL запитами на створення таблиць
    with open('1/create_table.sql', 'r') as f:
        sql_requests = f.read()

    # Виконуємо запити створення таблиць
    cur.execute(sql_requests)

    # Завершуємо транзакцію
    conn.commit()

    # Закриваємо з'єднання
    cur.close()

    print("Tables created successfully.")


if __name__ == "__main__":
    create_db()