from faker import Faker
from random import choice
from sqlalchemy import Column, Integer, ForeignKey, String, Sequence, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased, relationship, sessionmaker


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, autoincrement=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True)

    tasks = relationship("Tasks", back_populates="users", cascade="save-update, merge, delete")

    def __repr__(self):
        return f"User ({self.full_name}, {self.email})"


class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, Sequence('status_id_seq'), primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)

    tasks = relationship("Tasks", back_populates="status")

    def __repr__(self):
        return f"Status ({self.name})"


class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, Sequence('task_id_seq'), primary_key=True, autoincrement=True)
    title = Column(String(100))
    description = Column(Text)
    status_id = Column(Integer, ForeignKey("status.id"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    users = relationship("Users", back_populates="tasks")
    status = relationship("Status", back_populates="tasks")

    def __repr__(self):
        return f"Task ({self.title}, {self.description}, {self.status_id})"


class DatabaseManager:
    def __init__(self, engine):
        self.faker = Faker()
        self.engine = engine
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def delete_all_users(self):
        self.session.query(Users).delete()
        self.session.commit()

    def create_users(self, users_number: int):
        for i in range(users_number):
            full_name, email = self.faker.name(), self.faker.email()
            user = Users(full_name=full_name, email=email)
            self.session.add(user)
        self.session.commit()

    def get_all_users(self):
        return self.session.query(Users).all()

    def get_all_users_without_tasks(self):
        return self.session.query(Users).filter(Users.tasks == None).all()

    def get_users_by_email_pattern(self, pattern: str):
        return self.session.query(Users).filter(Users.email.like(f"%{pattern}%")).all()

    def get_users_by_task_status(self, status_name: str):
        return self.session.query(
            Users.id,
            Users.full_name,
            Users.email,
            Tasks.title,
            Tasks.description,
            Status.name.label('status')
        ).join(Tasks, Users.id == Tasks.user_id
               ).join(Status, Tasks.status_id == Status.id
                      ).filter(Status.name == status_name
                               ).all()

    def get_users_with_task_counts(self):
        result = self.session.query(
            Users.id,
            Users.full_name,
            Users.email,
            func.count(Tasks.id).label('task_count')
        ).outerjoin(Tasks, Users.id == Tasks.user_id
                    ).group_by(Users.id, Users.full_name, Users.email
                               ).all()

        return result

    def get_user_by_id(self, user_id: int):
        return self.session.query(Users).filter(Users.id == user_id).first()

    def get_random_user(self):
        users = self.get_all_users()
        return choice(users)

    def update_user(self, user_id: int, new_full_name: str = None, new_email: str = None):
        user = self.session.query(Users).filter(Users.id == user_id).first()
        if not new_full_name or new_full_name == "":
            new_full_name = self.faker.name()
        if not new_email or new_email == "":
            new_email = self.faker.email()
        user.full_name = new_full_name
        user.email = new_email
        self.session.commit()

    def create_statuses(self, status_list: list):
        for st_name in status_list:
            name = st_name
            status = Status(name=name)
            self.session.add(status)
        self.session.commit()

    def get_all_statuses(self):
        return self.session.query(Status).all()

    def get_random_status(self):
        statuses = self.get_all_statuses()
        return choice(statuses)

    def get_status_by_name(self, status_name: str):
        return self.session.query(Status).filter(Status.name == status_name).first()

    def delete_all_statuses(self):
        self.session.query(Status).delete()
        self.session.commit()

    def add_task_to_user(self, user_id: int, status_id: int):
        title = f"Task for User {user_id}"
        description = f"Description for Task for User {user_id}. {self.faker.text()}"
        statuses = self.get_all_statuses()
        task = Tasks(title=title, description=description, status_id=status_id, user_id=user_id)
        self.session.add(task)
        self.session.commit()

    def create_tasks(self, task_number: int):
        for i in range(task_number):
            title = f"Task {i + 1}"
            description = f"Description for Task {i + 1}. {self.faker.text()}"
            statuses = self.get_all_statuses()
            status_id = choice([status.id for status in statuses])
            users = self.get_all_users()
            user_id = choice([user.id for user in users])
            task = Tasks(title=title, description=description, status_id=status_id, user_id=user_id)
            self.session.add(task)
        self.session.commit()

    def get_all_tasks(self):
        return self.session.query(Tasks).all()

    def get_tasks_without_description(self):
        return self.session.query(Tasks).filter(Tasks.description == None).all()

    def get_tasks_not_done(self):
        done_status = self.session.query(Status).filter(Status.name == "Done").first()
        return self.session.query(Tasks).filter(Tasks.status_id != done_status.id).all()

    def get_tasks_of_user(self, user_id: int):
        return self.session.query(Tasks).filter(Tasks.user_id == user_id).all()

    def get_tasks_with_status(self, status_id: int):
        return self.session.query(Tasks).filter(Tasks.status_id == status_id).all()

    def get_tasks_of_users_with_email_pattern(self, pattern: str):
        result = self.session.query(
            Users.id,
            Users.full_name,
            Users.email,
            Tasks.title,
            Tasks.description,
            Status.name.label('status')
        ).join(Tasks, Users.id == Tasks.user_id
               ).join(Status, Tasks.status_id == Status.id
                      ).filter(Users.email.like(f"%{pattern}%")
                               ).all()

        return result

    def get_number_of_tasks_for_each_status(self):
        return self.session.query(Status.name, func.count(Tasks.id)).join(Tasks).group_by(Status.name).all()

    def get_random_task(self):
        tasks = self.get_all_tasks()
        return choice(tasks)

    def delete_all_tasks(self):
        self.session.query(Tasks).delete()
        self.session.commit()

    def delete_task(self, task_id: int):
        task = self.session.query(Tasks).filter(Tasks.id == task_id).first()
        self.session.delete(task)
        self.session.commit()

    def setup(self, users_number: int = 10, status_list: list = None, task_number: int = 10):
        if status_list is None:
            status_list = ["New", "In Progress", "Done"]
        self.delete_all_users()
        self.delete_all_statuses()
        self.delete_all_tasks()
        self.create_users(users_number)
        self.create_statuses(status_list)
        self.create_tasks(task_number)


