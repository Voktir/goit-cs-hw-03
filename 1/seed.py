from faker import Faker
from decor import db_connection

@db_connection
def seed_db(cur, conn):

    fake = Faker()


    # Заповнюємо таблиці випадковими значеннями

    statuses = ["new", "in progress", "completed"]
    for status in statuses:
        cur.execute(
            "INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
            (status,),
        )

    for _ in range(10):
        fullname = fake.name()
        email = fake.unique.email()
        cur.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s);",
            (fullname, email),
        )

    cur.execute("SELECT id FROM users;")
    user_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT id FROM status;")
    status_ids = [row[0] for row in cur.fetchall()]

    for _ in range(30):
        title = fake.sentence(nb_words=6)
        description = fake.text()
        status_id = fake.random_element(elements=status_ids)
        user_id = fake.random_element(elements=user_ids)
        cur.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
            (title, description, status_id, user_id),
        )

    # Підтверджуємо транзакцію
    conn.commit()

    # Закриваємо курсор та з'єднання
    cur.close()
    conn.close()

    print("Database seeded successfully.")


if __name__ == "__main__":
    seed_db()