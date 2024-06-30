from sqlalchemy.orm import sessionmaker


from db_engine import DBEngineFactory
from tables import TableHandler


POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "mypassword"
DB_NAME = "postgres"


def main():
    db_engine = DBEngineFactory.get_engine(
        db_type="postgres",
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        db=DB_NAME,
        echo=False
    )
    tb_handler = TableHandler(db_engine)
    tb_handler.setup(5, ["New", "In Progress", "Done"], 4)

    print("Get random user:".upper())
    user = tb_handler.get_random_user()
    print(user)
    print("Get all tasks of this user:".upper())
    tasks = tb_handler.get_tasks_of_user(user.id)
    for task in tasks:
        print("-" * 50)
        print(task)

    print("Get random status:".upper())
    status = tb_handler.get_random_status()
    print(status)
    print("Get all tasks with this status:".upper())
    tasks = tb_handler.get_tasks_with_status(status.id)
    for task in tasks:
        print("-" * 50)
        print(task)

    print("Get all users without tasks:".upper())
    users = tb_handler.get_all_users_without_tasks()
    if not users:
        print("All users have tasks")
    else:
        for user in users:
            print(user)


if __name__ == "__main__":
    main()
