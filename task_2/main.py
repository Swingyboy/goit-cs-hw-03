from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from pymongo.errors import CollectionInvalid, InvalidName, InvalidOperation, OperationFailure
import random
from typing import List


PASSWORD = "lNK5l8gTye5ccE9D"
URI = f"mongodb+srv://kedonosec:<password>@sbe-cluster.0wp1rac.mongodb.net/?appName=sbe-cluster"


class MongoConnector:
    def __init__(self, uri: str, password: str = None):
        if password:
            uri = uri.replace("<password>", password)
        self.client = MongoClient(uri)

    def get_client(self):
        try:
            res = self.client.admin.command('ping')
            if isinstance(res, dict) and res.get('ok') == 1.0:
                return self.client
            else:
                raise ValueError("Connection failed. Response: {res}")
        except Exception as e:
            raise ValueError(f"Connection failed: {e}")


class MongoDBManager:
    def __init__(self, uri: str, password: str):
        self._URI = uri
        self._PASSWORD = password
        self._collection = None
        self._client = None
        self._db = None

    def _check_connection(self):
        if not self._client:
            raise ValueError("Connection is not established")

    def _validate_schema(self, data: dict, is_updating: bool = False) -> tuple[bool, str]:
        expected_schema = {
            "name": (str, None),
            "age": (int, None),
            "features": (list, None)
        }
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        if not is_updating:
            for key, value_type in expected_schema.items():
                if key not in data:
                    return False, f"Missing key: {key}"
                if type(data[key]) not in value_type:
                    return False, f"Incorrect type for key: {key}, expected {value_type[0]}"
        for key in data.keys():
            if key not in expected_schema:
                return False, f"Unexpected key: {key}"

        return True, "Validated successfully"

    def create_db(self, db_name: str):
        self._check_connection()
        self._db = self._client[db_name]

    def create_collection(self, collection_name: str):
        self._check_connection()
        if self._db is None:
            raise ValueError("Database is not selected")
        try:
            print(f"Creating collection {collection_name}")
            self._db.create_collection(collection_name)
        except CollectionInvalid:
            print(f"Collection {collection_name} already exists")
            pass
        self._collection = self._db[collection_name]

    def add_one(self, name: str, age:int, features: List[str]) -> ObjectId:
        self._check_connection()
        if self._collection is None:
            raise ValueError("Collection is not selected")
        res = self._collection.insert_one({"name": name, "age": age, "features": features})
        return res.inserted_id

    def add_many(self, data: List[dict]) -> List[ObjectId]:
        for d in data:
            is_valid, msg = self._validate_schema(d)
            if not is_valid:
                raise ValueError(msg)
        res = self._collection.insert_many(data)
        return res.inserted_ids

    def get_all(self) -> List[dict]:
        self._check_connection()
        if self._collection is None:
            raise ValueError("Collection is not selected")
        res = list(self._collection.find())
        return res

    def get_by_id(self, _id: str) -> dict:
        self._check_connection()
        if self._collection is None:
            raise ValueError("Collection is not selected")
        return self._collection.find_one({"_id": ObjectId(_id)})

    def get_by_name(self, name: str) -> dict:
        self._check_connection()
        if self._collection is None:
            raise ValueError("Collection is not selected")
        return self._collection.find_one({"name": name})

    def update_by_id(self, _id: str, data: dict):
        res, msg = self._validate_schema(data, is_updating=True)
        if not res:
            raise ValueError(msg)
        self._check_connection()
        if self._collection is None:
            raise ValueError("Collection is not selected")
        self._collection.update_one({"_id": ObjectId(_id)}, {"$set": data})

    def update_by_name(self, name: str, data: dict):
        res, msg = self._validate_schema(data, is_updating=True)
        if not res:
            raise ValueError(msg)
        self._check_connection()
        if self._collection is None:
            raise ValueError("Collection is not selected")
        self._collection.update_one({"name": name}, {"$set": data})

    def delete_by_id(self, _id: str):
        self._check_connection()
        if self._collection is None:
            raise ValueError("Collection is not selected")
        self._collection.delete_one({"_id": ObjectId(_id)})

    def delete_by_name(self, name: str):
        self._check_connection()
        if self._collection is None:
            raise ValueError("Collection is not selected")
        self._collection.delete_one({"name":name})

    def delete_all(self):
        self._check_connection()
        if self._collection is None:
            raise ValueError("Collection is not selected")
        self._collection.delete_many({})

    def delete_collection(self):
        self._check_connection()
        if self._collection is None:
            raise ValueError("Collection is not selected")
        self._collection.drop()

    def drop_db(self):
        self._check_connection()
        if self._db is None:
            raise ValueError("Database is not selected")
        try:
            self._client.drop_database(self._db)
        except OperationFailure as e:
            print(f"Unable to drop database {self._db}")
            print(e.details)
            pass

    @classmethod
    def connect(cls, uri: str, password: str):
        obj = cls(uri, password)
        obj._client = MongoConnector(uri, password).get_client()
        return obj

    def disconnect(self, erase: bool = False):
        if erase:
            self.delete_collection()
            self.drop_db()
        self._client.close()
        self._client = None


def seed_db(db_manager, records: int):
    cat_names = ["Tom", "Jerry", "Garfield", "Simba", "Nala", "Mufasa", "Bagheera", "Baloo", "Shere Khan", "Rajah"]
    cat_features = ["cute", "playful", "lazy", "hungry", "sleepy", "curious", "friendly", "agile", "independent"]
    for i in range(records):
        name = random.choice(cat_names)
        age = random.randint(1, 20)
        features = random.sample(cat_features, random.randint(1, 5))
        db_manager.add_one(name, age, features)


def clear_db(db_manager):
    db_manager.delete_all()


def main():
    db_manager = MongoDBManager.connect(URI, PASSWORD)
    db_manager.create_db("cats_db")
    db_manager.create_collection("cats")
    seed_db(db_manager, 10)
    print(list(db_manager.get_all()))
    clear_db(db_manager)
    db_manager.disconnect()


if __name__ == "__main__":
    main()
