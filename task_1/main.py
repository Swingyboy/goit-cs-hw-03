from sqlalchemy.orm import sessionmaker


from db_engine import DBEngineFactory
from tables import DatabaseManager

RED_COLOR = "\033[91m"
WHITE_COLOR = "\033[0m"
GREEN_COLOR = "\033[92m"
YELLOW_COLOR = "\033[93m"

POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "mypassword"
DB_NAME = "postgres"


def print_items(items):
    if not items:
        print(RED_COLOR + "No records found in data base".upper() + WHITE_COLOR)
    else:
        for item in items:
            print("-" * 50)
            print(item)


def task_1(manager):
    """Get random user and all tasks of this user."""
    print(GREEN_COLOR + "Get random user:".upper() + WHITE_COLOR)
    random_user = manager.get_random_user()
    print(random_user)
    print("Get all tasks of this user:".upper())
    tasks = manager.get_tasks_of_user(random_user.id)
    print_items(tasks)


def task_2(manager):
    """Get status and all tasks with this status."""
    input_status = input(YELLOW_COLOR + "Enter status: " + WHITE_COLOR)
    status = manager.get_status_by_name(input_status)
    print(status)
    if not status:
        print(RED_COLOR + "No status found".upper() + WHITE_COLOR)
        return
    print(GREEN_COLOR + "Get all tasks with this status:".upper() + WHITE_COLOR)
    tasks = manager.get_tasks_with_status(status.id)
    print_items(tasks)


def task_3(manager):
    """Update task status"""


def task_4(manager):

    print(GREEN_COLOR + "Get all users without tasks:".upper() + WHITE_COLOR)
    users = manager.get_all_users_without_tasks()
    print_items(users)


def task_5(manager):
    random_user = manager.get_random_user()
    random_status = manager.get_random_status()
    print(GREEN_COLOR + "Add a new task to ".upper() + str(random_user) + " with ".upper() + str(random_status) + WHITE_COLOR)
    manager.add_task_to_user(random_user.id, random_status.id)
    tasks = manager.get_tasks_of_user(random_user.id)
    print_items(tasks)


def task_6(manager):
    print(GREEN_COLOR + "Get all tasks these are not done".upper() + WHITE_COLOR)
    not_done_tasks = manager.get_tasks_not_done()
    print(not_done_tasks)


def task_7(manager):
    print(GREEN_COLOR + "Get random task".upper() + WHITE_COLOR)
    random_task = manager.get_random_task()
    print(random_task)
    print(GREEN_COLOR + "Delete this task".upper() + WHITE_COLOR)
    manager.delete_task(random_task.id)
    tasks = manager.get_all_tasks()
    print_items(tasks)


def task_8(manager):
    email_pattern = input(YELLOW_COLOR + "Enter email pattern: " + WHITE_COLOR)
    if not email_pattern:
        email_pattern = "gmail.com"
    print(GREEN_COLOR + "Get all users with email like: ".upper() + email_pattern + WHITE_COLOR)
    users = manager.get_users_by_email_pattern(email_pattern)
    print_items(users)


def task_9(manager):
    random_user = manager.get_random_user()
    print(GREEN_COLOR + "Update user".upper() + str(random_user) + WHITE_COLOR)
    new_full_name = input(YELLOW_COLOR + "Enter new full name: " + WHITE_COLOR)
    new_email = input(YELLOW_COLOR + "Enter new email: " + WHITE_COLOR)
    manager.update_user(random_user.id, new_full_name, new_email)
    print(GREEN_COLOR + "User was updated" + WHITE_COLOR)
    print(manager.get_user_by_id(random_user.id))


def task_10(manager):
    print(GREEN_COLOR + "Get number of tasks for each status".upper() + WHITE_COLOR)
    tasks_number = manager.get_number_of_tasks_for_each_status()
    for number in tasks_number:
        print(number[0], number[1])


def task_11(manager):
    print(GREEN_COLOR + "Get tasks of users with email pattern".upper() + WHITE_COLOR)
    pattern = input(YELLOW_COLOR + "Enter email pattern: " + WHITE_COLOR)
    if not pattern:
        pattern = "gmail.com"
    tasks = manager.get_tasks_of_users_with_email_pattern(pattern)
    print_items(tasks)


def task_12(manager):
    print(GREEN_COLOR + "Get all tasks without description".upper() + WHITE_COLOR)
    tasks = manager.get_tasks_without_description()
    print_items(tasks)


def task_13(manager, status="In Progress"):
    print(GREEN_COLOR + "Get users with task with status: ".upper() + status + WHITE_COLOR)
    users = manager.get_users_by_task_status(status)
    print_items(users)


def task_14(manager):
    print(GREEN_COLOR + "Get all users with task counts".upper() + WHITE_COLOR)
    users = manager.get_users_with_task_counts()
    print_items(users)


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
    database_manager = DatabaseManager(db_engine)
    database_manager.setup(5, ["New", "In Progress", "Done"], 4)
    task_1(database_manager)
    task_2(database_manager)
    task_3(database_manager)
    task_4(database_manager)
    task_5(database_manager)
    task_6(database_manager)
    task_7(database_manager)
    task_8(database_manager)
    task_9(database_manager)
    task_10(database_manager)
    task_11(database_manager)
    task_12(database_manager)
    task_13(database_manager)
    task_14(database_manager)


if __name__ == "__main__":
    main()
