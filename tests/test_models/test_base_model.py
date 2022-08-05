#!/usr/bin/python3
"""This module contains unittest code for the base_model module"""


import io
import os
import sys
from time import sleep
from unittest.mock import patch
import uuid
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime

import unittest

storage = FileStorage()
storage.all().clear()
storage.save()


def fake_uuid4():
    return "1"


class fake_datetime(datetime):

    @classmethod
    def today(cls):
        return cls.fromtimestamp(1666666666)


class TestBaseModelInit(unittest.TestCase):

    def setUp(self):
        try:
            os.remove("file.json")
        except BaseException:
            pass
        storage.all().clear()
        storage.save()

    @patch('uuid.uuid4', fake_uuid4)
    def test_init_id(self):
        obj = BaseModel()
        self.assertEqual(obj.id, "1")

    @patch('datetime.datetime', fake_datetime)
    def test_init_created_at(self):
        test_date = datetime.fromtimestamp(1666666666)
        obj = BaseModel()
        self.assertEqual(obj.created_at, test_date)

    @patch('datetime.datetime', fake_datetime)
    def test_init_updated_at(self):
        test_date = datetime.fromtimestamp(1666666666)
        obj = BaseModel()
        self.assertEqual(obj.updated_at, test_date)

    def test_init_with_args_str(self):
        obj = BaseModel("some random string")
        self.assertTrue("some random string" not in obj.__dict__.values())

    def test_init_with_args_none(self):
        obj = BaseModel(None)
        self.assertTrue(None not in obj.__dict__.values())

    def test_init_with_kwargs_id(self):
        obj_id = str(uuid.uuid4())
        obj = BaseModel(id=obj_id)
        self.assertEqual(obj.id, obj_id)

    def test_init_with_kwargs_created_at(self):
        date = datetime.today()
        obj = BaseModel(created_at=datetime.isoformat(date))
        self.assertEqual(obj.created_at, date)

    def test_init_with_kwargs_updated_at(self):
        date = datetime.today()
        obj = BaseModel(updated_at=datetime.isoformat(date))
        self.assertEqual(obj.updated_at, date)

    def test_init_with_kwargs_None_value(self):
        self.assertEqual(None, BaseModel(id=None).id)
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_init_with_multiple_kwargs(self):
        created_at = datetime.today()
        updated_at = datetime.today()
        obj_id = str(uuid.uuid4())
        obj = BaseModel(id=obj_id, created_at=datetime.isoformat(created_at),
                        updated_at=datetime.isoformat(updated_at))
        self.assertEqual(obj.id, obj_id)
        self.assertEqual(obj.created_at, created_at)
        self.assertEqual(obj.updated_at, updated_at)

    def test_init_with_args_and_kwargs(self):
        created_at = datetime.today()
        updated_at = datetime.today()
        obj_id = str(uuid.uuid4())
        obj = BaseModel(
            "some random string",
            id=obj_id,
            created_at=datetime.isoformat(created_at),
            updated_at=datetime.isoformat(updated_at))
        self.assertNotIn('some random string', obj.__dict__.values())
        self.assertEqual(obj.id, obj_id)
        self.assertEqual(obj.created_at, created_at)
        self.assertEqual(obj.updated_at, updated_at)

    def test_created_at_is_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_created_at_change(self):
        obj1 = BaseModel()
        sleep(0.01)
        obj2 = BaseModel()
        self.assertTrue(obj2.created_at > obj1.created_at)

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_updated_at_change(self):
        obj1 = BaseModel()
        sleep(0.01)
        obj2 = BaseModel()
        self.assertTrue(obj2.updated_at > obj1.updated_at)

    def test_objects_uniqueness(self):
        self.assertNotEqual(BaseModel().id, BaseModel().id)


class TestBaseModelStringRepresentation(unittest.TestCase):
    def setUp(self):
        try:
            os.remove("file.json")
        except BaseException:
            pass
        storage.all().clear()
        storage.save()

    @patch('sys.stdout', io.StringIO())
    @patch('datetime.datetime', fake_datetime)
    @patch('uuid.uuid4', fake_uuid4)
    def test_str_rep_no_args(self):
        obj = BaseModel()
        print(obj, end="")
        fake_date = fake_datetime.today().__repr__()
        must_have = [
            "[BaseModel] (1)",
            "'id': '1'",
            "'created_at': {}".format(fake_date),
            "'updated_at': {}".format(fake_date)]
        stdout_value = sys.stdout.getvalue()

        for item in must_have:
            self.assertTrue(item in stdout_value)


class TestBaseModelSave(unittest.TestCase):
    def setUp(self):
        try:
            os.remove("file.json")
        except BaseException:
            pass
        storage.all().clear()
        storage.save()

    def test_save_changes_updated_at(self):
        obj = BaseModel()
        first_updated_at = obj.updated_at
        sleep(0.1)
        obj.save()
        self.assertTrue(obj.updated_at > first_updated_at)

    def test_save_store_obj_in_file(self):
        os.unlink('file.json')
        storage.reload()
        obj = BaseModel()
        obj.save()
        with open("file.json", "r", encoding="utf-8") as file:
            self.assertTrue("BaseModel.{}".format(obj.id) in file.read())
        pass

    def test_save_with_one_arg(self):
        obj = BaseModel()
        with self.assertRaises(TypeError):
            obj.save("some random string")


class TestBaseModelToDict(unittest.TestCase):
    def setUp(self):
        try:
            os.remove("file.json")
        except BaseException:
            pass
        storage.all().clear()
        storage.save()

    def test_to_dict_with_arg(self):
        obj = BaseModel()
        with self.assertRaises(TypeError):
            obj.to_dict("some random arg")

    @patch('uuid.uuid4', fake_uuid4)
    @patch('datetime.datetime', fake_datetime)
    def test_to_dict(self):
        obj = BaseModel()
        exp_dict = {
            'id': fake_uuid4(),
            '__class__': 'BaseModel',
            'created_at': fake_datetime.today().isoformat(),
            'updated_at': fake_datetime.today().isoformat()
        }
        self.assertDictEqual(obj.to_dict(), exp_dict)

    def test_to_dict_holds_the_right_values(self):
        obj = BaseModel()
        dict_rep = obj.to_dict()
        self.assertEqual(obj.id, dict_rep["id"])
        self.assertEqual("BaseModel", dict_rep["__class__"])
        self.assertEqual(datetime.isoformat(
            obj.created_at), dict_rep["created_at"])
        self.assertEqual(datetime.isoformat(
            obj.updated_at), dict_rep["updated_at"])

    def test_to_dict_hold_the_right_keys(self):
        obj = BaseModel()
        keys = obj.to_dict().keys()
        self.assertIn("updated_at", keys)
        self.assertIn("created_at", keys)
        self.assertIn("id", keys)
        self.assertIn("__class__", keys)

    def test_to_dict_value_are_of_right_type(self):
        obj = BaseModel()
        dict_rep = obj.to_dict()
        self.assertEqual(str, type(dict_rep["id"]))
        self.assertEqual(str, type(dict_rep["__class__"]))
        self.assertEqual(str, type(dict_rep["updated_at"]))
        self.assertEqual(str, type(dict_rep["created_at"]))


if __name__ == "__main__":
    unittest.main()
