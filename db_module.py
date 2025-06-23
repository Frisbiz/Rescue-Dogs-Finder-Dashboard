"""
db_module.py
MongoDB helper for the AAC collection.
Adds environment‑driven connection strings and basic connection checks.
Third enhancement: stronger configuration and error handling.
"""

import os
from typing import Any, List
from pymongo import MongoClient, errors


class AnimalShelter:
    """CRUD wrapper for the AAC.animals collection."""

    def __init__(self) -> None:
        # third enhancement: read connection info from env vars
        uri = os.getenv("AAC_MONGO_URI", "mongodb://localhost:27018")
        db_name = os.getenv("AAC_DB", "AAC")
        col_name = os.getenv("AAC_COL", "animals")

        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            # third enhancement: immediately test the connection
            self.client.admin.command("ping")
        except errors.PyMongoError as exc:
            # fail fast with a clear message
            raise RuntimeError(f"Cannot connect to MongoDB: {exc}") from exc

        self.database = self.client[db_name]
        self.collection = self.database[col_name]

    # ---------- CRUD ----------
    def create(self, data: dict[str, Any]) -> bool:
        if not data:
            return False
        try:
            self.collection.insert_one(data)
            return True
        except errors.PyMongoError as exc:
            print(f"[create] {exc}")
            return False

    def read(self, query: dict | None = None) -> List[dict]:
        try:
            return list(self.collection.find(query or {}, {"_id": False}))
        except errors.PyMongoError as exc:
            print(f"[read] {exc}")
            return []

    def update(self, query: dict, new_values: dict) -> int:
        try:
            res = self.collection.update_many(query, {"$set": new_values})
            return res.modified_count
        except errors.PyMongoError as exc:
            print(f"[update] {exc}")
            return 0

    def delete(self, query: dict) -> int:
        try:
            res = self.collection.delete_many(query)
            return res.deleted_count
        except errors.PyMongoError as exc:
            print(f"[delete] {exc}")
            return 0
