from decor import db_connection

@db_connection
def execute_sql_file(cur, conn):

    with open('1/req_to_tables.sql', 'r', encoding="UTF-8") as f:
        sql_script = f.read()

    # Розбиваємо скрипт на окремі запити (припускаємо, що кожен запит закінчується ';')
    queries = sql_script.split('\n')
    # print(queries)

    for query in queries:
        print(query)
        if query and (not query.startswith('--')):  # Ігноруємо пусті рядки та коменти
            cur.execute(query)
            print(f"Запит виконано: {query}")

    # Завершення роботи з курсором і з'єднанням
    cur.close()
    conn.commit()

if __name__ == "__main__":
    execute_sql_file()
