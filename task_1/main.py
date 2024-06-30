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
    """Get user and all tasks of this user."""
    users = manager.get_all_users()
    print(GREEN_COLOR + "Available users:".upper() + WHITE_COLOR)
    print_items(users)
    user_id = input(YELLOW_COLOR + "Enter user id: " + WHITE_COLOR)
    print("Get all tasks of this user:".upper())
    tasks = manager.get_tasks_of_user(user_id)
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
    tasks = manager.get_all_tasks()
    print(GREEN_COLOR + "Available tasks:".upper() + WHITE_COLOR)
    print_items(tasks)
    task_id = input(YELLOW_COLOR + "Enter task id: " + WHITE_COLOR)
    new_status = input(YELLOW_COLOR + "Enter new status: " + WHITE_COLOR)
    manager.update_task_status(task_id, new_status)
    task = manager.get_task_by_id(task_id)
    print(GREEN_COLOR + "Task was updated".upper() + WHITE_COLOR)
    print(task)


def task_4(manager):
    """Get all users without tasks."""
    print(GREEN_COLOR + "Get all users without tasks:".upper() + WHITE_COLOR)
    users = manager.get_all_users_without_tasks()
    print_items(users)


def task_5(manager):
    """Add a new task  with status to user."""
    users = manager.get_all_users()
    print(GREEN_COLOR + "Available users:".upper() + WHITE_COLOR)
    print_items(users)
    user_id = input(YELLOW_COLOR + "Enter user id: " + WHITE_COLOR)
    input_status = input(YELLOW_COLOR + "Enter status: " + WHITE_COLOR)
    status = manager.get_status_by_name(input_status)
    if not status:
        print(RED_COLOR + "No status found".upper() + WHITE_COLOR)
        return
    print(GREEN_COLOR + "Add a new task to user with id".upper() + str(user_id) +
          " with ".upper() + str(status) + WHITE_COLOR)
    manager.add_task_to_user(user_id, status.id)
    tasks = manager.get_tasks_of_user(status.id)
    print_items(tasks)


def task_6(manager):
    """Get all tasks these are not done."""
    print(GREEN_COLOR + "Get all tasks these are not done".upper() + WHITE_COLOR)
    not_done_tasks = manager.get_tasks_not_done()
    print(not_done_tasks)


def task_7(manager):
    """Delete specified task."""
    print(GREEN_COLOR + "Available tasks:".upper() + WHITE_COLOR)
    tasks = manager.get_all_tasks()
    print_items(tasks)
    task_id = input(YELLOW_COLOR + "Enter task id: " + WHITE_COLOR)
    print(GREEN_COLOR + "Delete this task".upper() + WHITE_COLOR)
    manager.delete_task(task_id)
    tasks = manager.get_all_tasks()
    print_items(tasks)


def task_8(manager):
    """Get all users with email pattern."""
    email_pattern = input(YELLOW_COLOR + "Enter email pattern: " + WHITE_COLOR)
    if not email_pattern:
        email_pattern = "gmail.com"
    print(GREEN_COLOR + "Get all users with email like: ".upper() + email_pattern + WHITE_COLOR)
    users = manager.get_users_by_email_pattern(email_pattern)
    print_items(users)


def task_9(manager):
    """Update user."""
    print(GREEN_COLOR + "Available users:".upper() + WHITE_COLOR)
    users = manager.get_all_users()
    print_items(users)
    user_id = input(YELLOW_COLOR + "Enter user id: " + WHITE_COLOR)
    print(GREEN_COLOR + "Update user ".upper() + str(user_id) + WHITE_COLOR)
    new_full_name = input(YELLOW_COLOR + "Enter new full name: " + WHITE_COLOR)
    new_email = input(YELLOW_COLOR + "Enter new email: " + WHITE_COLOR)
    manager.update_user(user_id, new_full_name, new_email)
    print(GREEN_COLOR + "User was updated" + WHITE_COLOR)
    print(manager.get_user_by_id(user_id))


def task_10(manager):
    """Get number of tasks for each status."""
    print(GREEN_COLOR + "Get number of tasks for each status".upper() + WHITE_COLOR)
    tasks_number = manager.get_number_of_tasks_for_each_status()
    for number in tasks_number:
        print(number[0], number[1])


def task_11(manager):
    """Get tasks of users with email pattern."""
    print(GREEN_COLOR + "Get tasks of users with email pattern".upper() + WHITE_COLOR)
    pattern = input(YELLOW_COLOR + "Enter email pattern: " + WHITE_COLOR)
    if not pattern:
        pattern = "gmail.com"
    tasks = manager.get_tasks_of_users_with_email_pattern(pattern)
    print_items(tasks)


def task_12(manager):
    """Get all tasks without description."""
    print(GREEN_COLOR + "Get all tasks without description".upper() + WHITE_COLOR)
    tasks = manager.get_tasks_without_description()
    print_items(tasks)


def task_13(manager, status="In Progress"):
    """Get users with task with status."""
    print(GREEN_COLOR + "Get users with task with status: ".upper() + status + WHITE_COLOR)
    users = manager.get_users_by_task_status(status)
    print_items(users)


def task_14(manager):
    """Get all users with task counts."""
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
    users_number = input(YELLOW_COLOR + "Enter number of users these would be added to database: " + WHITE_COLOR)
    if not users_number:
        print(RED_COLOR + "No correct number of users were provided".upper() + WHITE_COLOR)
        print(GREEN_COLOR + "Default number of users will be used".upper() + WHITE_COLOR)
        users_number = 10
    else:
        users_number = int(users_number)

    status_list = input(YELLOW_COLOR + "Enter list of statuses separated by comma: " + WHITE_COLOR)
    if not status_list:
        print(RED_COLOR + "No correct statuses were provided".upper() + WHITE_COLOR)
        print(GREEN_COLOR + "Default statuses will be used".upper() + WHITE_COLOR)
        status_list = ["New", "In Progress", "Done"]
    else:
        status_list = status_list.split(",")
        status_list = [status.capitalize() for status in status_list]

    task_number = input(YELLOW_COLOR + "Enter number of tasks these would be added to database: " + WHITE_COLOR)
    if not task_number:
        print(RED_COLOR + "No correct number of tasks were provided".upper() + WHITE_COLOR)
        print(GREEN_COLOR + "Default number of tasks will be used".upper() + WHITE_COLOR)
        task_number = 10
    else:
        task_number = int(task_number)
    print(GREEN_COLOR + "Setup database...".upper() + WHITE_COLOR)
    database_manager.setup(users_number, status_list, task_number)
    home_task_dict = {
        1: task_1,
        2: task_2,
        3: task_3,
        4: task_4,
        5: task_5,
        6: task_6,
        7: task_7,
        8: task_8,
        9: task_9,
        10: task_10,
        11: task_11,
        12: task_12,
        13: task_13,
        14: task_14
    }
    while True:
        try:
            print(GREEN_COLOR + "Available home tasks:".upper() + WHITE_COLOR)
            for key, value in home_task_dict.items():
                print(f"{key}: {value.__doc__}")
            task_number = input(YELLOW_COLOR + "Enter task number: " + WHITE_COLOR)
            if not task_number:
                print(RED_COLOR + "No task number was provided".upper() + WHITE_COLOR)
                print(GREEN_COLOR + "Exit".upper() + WHITE_COLOR)
                break
            task_number = int(task_number)
            if task_number not in home_task_dict:
                print(RED_COLOR + "No task with this number".upper() + WHITE_COLOR)
                print(GREEN_COLOR + "Exit".upper() + WHITE_COLOR)
                break
            home_task_dict[task_number](database_manager)
            cont = input(YELLOW_COLOR + "Do you want to continue? (yes/no): " + WHITE_COLOR)
            if cont.lower() in ["no", "n"]:
                print(GREEN_COLOR + "Exit".upper() + WHITE_COLOR)
                break
        except KeyboardInterrupt:
            print(RED_COLOR + "Exit".upper() + WHITE_COLOR)
            break
        except ValueError as e:
            print(RED_COLOR + f"Error: {e}".upper() + WHITE_COLOR)
            print(GREEN_COLOR + "Exit".upper() + WHITE_COLOR)
            break


if __name__ == "__main__":
    main()
