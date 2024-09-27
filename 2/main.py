from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

# Підключення до MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["cat_database"]
    collection = db["cats"]
    # Перевірка з'єднання
    client.admin.command('ismaster')
    print("MongoDB підключено успішно")
except ConnectionFailure:
    print("Не вдалося підключитися до MongoDB, перевірте з'єднання")


def db_operation_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PyMongoError as e:
            print(f"Помилка при роботі з MongoDB: {e}")
        except ValueError as e:
            print(f"Помилка введення: {e}")
    return inner

@db_operation_error
def create_cat(name:str, age:int, features:list[str]):
    cat = {"name": name, "age": age, "features": features}
    print(cat)
    collection.insert_one(cat)
    print(f"Кицька {name} додана до бази")

@db_operation_error
def read_all_cats():
    cats = collection.find()
    print("В базі маємо такі записи")
    for cat in cats:
        print(cat)

@db_operation_error
def read_cat_by_name(name: str):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"Кицьку на ім'я {name} не знайдено")

@db_operation_error
def update_cat_age(name: str, new_age: int):
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count > 0:
        print(f"Вік кицьки {name} оновлено на {new_age}")
    else:
        print(f"Кицьку на ім'я {name} не знайдено")

@db_operation_error
def add_feature_to_cat(name: str, feature: str):
    result = collection.update_one({"name": name}, {"$push": {"features": feature}})
    if result.matched_count > 0:
        print(f"Кицькі '{name}' було додано особливість {feature}")
    else:
        print(f"Кицьку на ім'я {name} не знайдено")

@db_operation_error
def delete_cat(name: str):
    result = collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Кицька {name} була видалена з бази")
    else:
        print(f"Кицьку на ім'я {name} не знайдено")

@db_operation_error
def delete_all_cats():
    result = collection.delete_many({})
    print(f"Всі записи було видалено. Загальна кількість видалених записів: {result.deleted_count}")

def main():
    while True:
        print("\nДоступні дії:")
        print("1 - Створити запис про тварину")
        print("2 - Показати всі записи")
        print("3 - Пошук запису за ім'ям тварини")
        print("4 - Оновити вік тварини")
        print("5 - Додати особливість до тварини")
        print("6 - Видалити запис про тварину")
        print("7 - Видалити всі записи")
        print("8 - Вийти")
        choice = input("Виберіть дію: ")

        match choice:
            case "1":
                name = input("Вкажіть ім'я: ")
                age = int(input("Вкажіть вік: "))
                features = input("Вкажіть особливості улюбленця (через кому): ").split(",")
                create_cat(name, age, features)
            case "2":
                read_all_cats()
            case "3":
                name = input("Вкажіть ім'я: ")
                read_cat_by_name(name)
            case "4":
                name = input("Вкажіть ім'я: ")
                new_age = int(input("Вкажіть вік: "))
                update_cat_age(name, new_age)
            case "5":
                name = input("Вкажіть ім'я: ")
                feature = input("Вкажіть особливість: ")
                add_feature_to_cat(name, feature)
            case "6":
                name = input("Вкажіть ім'я: ")
                delete_cat(name)
            case "7":
                delete_all_cats()
            case "8":
                break
            case _:
                print("Не вірна команда, спробуйте ще.")

if __name__ == "__main__":
    main()




