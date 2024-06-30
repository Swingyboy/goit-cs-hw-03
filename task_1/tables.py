from faker import Faker
from random import choice
from sqlalchemy import Column, Integer, ForeignKey, String, Sequence, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


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


class TableHandler:
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

    def get_random_user(self):
        users = self.get_all_users()
        return choice(users)

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

    def delete_all_statuses(self):
        self.session.query(Status).delete()
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

    def get_tasks_of_user(self, user_id: int):
        return self.session.query(Tasks).filter(Tasks.user_id == user_id).all()

    def get_tasks_with_status(self, status_id: int):
        return self.session.query(Tasks).filter(Tasks.status_id == status_id).all()

    def delete_all_tasks(self):
        self.session.query(Tasks).delete()
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


