import psycopg2

host = "localhost"
dbname = "postgres"
user = "postgres"
password="my_pass"

def db_connection(func):
    def inner(*args, **kwargs):
        conn = None
        try:
            # Підключаємось до бази даних
            conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
            cur = conn.cursor()

            return func(cur, conn, *args, **kwargs)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    return inner
