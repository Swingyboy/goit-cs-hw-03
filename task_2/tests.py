from unittest import TestCase
from main import MongoDBManager, seed_db, clear_db

PASSWORD = "lNK5l8gTye5ccE9D"
URI = f"mongodb+srv://kedonosec:<password>@sbe-cluster.0wp1rac.mongodb.net/?appName=sbe-cluster"

class TestMongoDBManager(TestCase):
    def setUp(self) -> None:
        self.db_manager = MongoDBManager.connect(URI, PASSWORD)
        self.db_manager.create_db("cats")
        self.db_manager.create_collection("cats_collection")
        clear_db(self.db_manager)

    def test_add_one(self):
        data = {
            "name": "John",
            "age": 2,
            "features": ["smart", "handsome"]
        }
        self.db_manager.add_one(data["name"], data["age"], data["features"])
        self.assertEqual(len(self.db_manager.get_all()), 1)

    def test_add_many(self):
        data = [
            {
                "name": "John",
                "age": 2,
                "features": ["smart", "handsome"]
            },
            {
                "name": "Jane",
                "age": 3,
                "features": ["smart", "beautiful"]
            }
        ]
        self.db_manager.add_many(data)
        self.assertEqual(len(self.db_manager.get_all()),  2)

    def test_get_all(self):
        data = [
            {
                "name": "John",
                "age": 2,
                "features": ["smart", "handsome"]
            },
            {
                "name": "Jane",
                "age": 3,
                "features": ["smart", "beautiful"]
            }
        ]
        self.db_manager.add_many(data)
        self.assertEqual(len(self.db_manager.get_all()), 2)

    def test_get_by_id(self):
        data = {
            "name": "John",
            "age": 2,
            "features": ["smart", "handsome"]
        }
        _id = self.db_manager.add_one(**data)
        res = self.db_manager.get_by_id(_id)
        self.assertEqual(res["name"], data["name"])
        self.assertEqual(res["age"], data["age"])
        self.assertEqual(res["features"], data["features"])

    def test_get_by_name(self):
        data = {
            "name": "Vasyl",
            "age": 2,
            "features": ["smart", "handsome"]
        }
        self.db_manager.add_one(**data)
        res = self.db_manager.get_by_name(data["name"])
        self.assertEqual(res["name"], data["name"])
        self.assertEqual(res["age"], data["age"])
        self.assertEqual(res["features"], data["features"])

    def test_update_by_id(self):
        data = {
            "name": "John",
            "age": 2,
            "features": ["smart", "handsome"]
        }
        _id = self.db_manager.add_one(**data)
        self.db_manager.update_by_id(_id, {"name": "John Doe"})
        self.assertEqual(self.db_manager.get_by_id(_id)["name"], "John Doe")

    def test_update_by_name(self):
        data = {
            "name": "John",
            "age": 2,
            "features": ["smart", "handsome"]
        }
        self.db_manager.add_one(**data)
        self.db_manager.update_by_name(data["name"], {"name": "John Doe"})
        self.assertEqual(self.db_manager.get_by_name("John Doe")["name"], "John Doe")

    def test_delete_by_id(self):
        data = {
            "name": "John",
            "age": 2,
            "features": ["smart", "handsome"]
        }
        _id = self.db_manager.add_one(**data)
        self.db_manager.delete_by_id(_id)
        self.assertEqual(len(self.db_manager.get_all()), 0)

    def test_delete_by_name(self):
        data = {
            "name": "John",
            "age": 2,
            "features": ["smart", "handsome"]
        }
        self.db_manager.add_one(**data)
        self.db_manager.delete_by_name(data["name"])
        self.assertEqual(len(self.db_manager.get_all()), 0)




