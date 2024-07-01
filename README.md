# GoIT. Computer Science. Homework 3
## Description
This repository contains the solutions to the tasks of the third homework of the Computer Science course at GoIT.
## Dependencies
The script uses the following dependencies:
 - **psycopg2** - PostgreSQL database adapter for Python
 - **sqlalchemy** - SQL toolkit and Object-Relational Mapping (ORM) library for Python
 - **faker** - Faker is a Python package that generates fake data
 - **pymongo** - Python driver for MongoDB
## Tasks
### Task 1
The script connects to the local Postgres database and creates (if it doesn't exist) 3 tables:
 - **Users**
 - **Status**
 - **Tasks**
After that it requests the number of users, the coma separated list of statuses and the number of tasks to generate. The script generates the specified number of users, statuses and tasks and inserts them into the corresponding tables.
After initialization, the script displays the available tasks from homework and requests the task number to execute.
 - **Task 1** - The script displays the list of users, requests any id of existed users and displays the list of task for this user.
 - **Task 2** - The script displays the list of statuses, requests any id of existed statuses and displays the list of tasks with this status.
 - **Task 3** - The script displays the list of tasks, requests any id of existed tasks and new status for this task. After that, the script updates the status of the task.
 - **Task 4** - The script displays the list of users without tasks
 - **Task 5** - The script adds a new task to the user. The script requests the user id and status. After that, the script adds the task to the user.
 - **Task 6** - The script displays all task without "Done" status.
 - **Task 7** - The script displays the list of tasks, requests any id of existed tasks and deletes this task.
 - **Task 8** - The script requests email pattern and displays the list of users with email matching the pattern.
 - **Task 9** - The script requests the user id after that requests new name and email for this user. After that, the script updates the user.
 - **Task 10** - The script displays the number of tasks for each user.
 - **Task 11** - The script requests email pattern and displays the list of tasks with users email matching the pattern.
 - **Task 12** - The script displays the list of tasks without description.
 - **Task 13** - The script requests the status name and displays the list of tasks with this status.
 - **Task 14** - The script displays the task count for each user.
### Task 2
The script implements Mongo DB Manager that supports the next commands:
 - **disconnect** - disconnects from the MongoDB
 - **connect** - class method for connecting to the MongoDB
 - **create_db** - creates a new database
 - **create_collection** - creates a new collection
 - **add_one** - adds a new document to the collection
 - **add_many** - adds multiple documents to the collection
 - **get_all** - gets all documents from the collection
 - **get_by_id** - gets the document by id
 - **get_by_name** - gets the document by name
 - **update_by_id** - updates the document by id
 - **update_by_name** - updates the document by name
 - **delete_by_id** - deletes the document by id
 - **delete_by_name** - deletes the document by name
 - **delete_all** - deletes all documents from the collection
 - **delete_collection** - deletes the collection
 - **delete_db** - deletes the database

The manager accepts the document in the next format:
```json
{
    "name": "Tom",
    "age": 2,
    "city": ["fat", "lazy"]
}
```

If main.py runs as script it would expect URI and password for Mongo DB as input params.
After that the script creates a new database "cats_db" and collection "cats" in it, and seeds the collection with 10 documents.
After that it prints the list of created documents and clears the collection.
## Installation
1. Clone the repository
```bash
git clone https://github.com/Swingyboy/goit-cs-hw-03.git
```
2. Create a virtual environment
```bash
python3 -m venv venv
```
3. Activate the virtual environment
```bash
source venv/bin/activate
```
4. Install the requirements
```bash
pip install -r requirements.txt
```
## Usage
### Task 1
```bash
cd task1
```
```bash
python3 main.py
```
### Task 2
As a script
```bash
python3 main.py --uri mongodb://localhost:27017/ --password mypassword
```
As a module
```python
from task2.main import MongoManager

manager = MongoManager.connect(uri, password)
```