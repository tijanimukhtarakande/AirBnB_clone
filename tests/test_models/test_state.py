#!/usr/bin/python3
"""This module contains unittest code for the state module"""


import io
import os
import sys
from time import sleep
from unittest.mock import patch
import uuid
from models.state import State
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


class TestStateInit(unittest.TestCase):

    @patch('uuid.uuid4', fake_uuid4)
    def test_init_id(self):
        obj = State()
        self.assertEqual(obj.id, "1")

    def test_init_add_to_storage(self):
        obj = State()
        self.assertTrue(obj in storage.all().values())

    @patch('datetime.datetime', fake_datetime)
    def test_init_created_at(self):
        test_date = datetime.fromtimestamp(1666666666)
        obj = State()
        self.assertEqual(obj.created_at, test_date)

    @patch('datetime.datetime', fake_datetime)
    def test_init_updated_at(self):
        test_date = datetime.fromtimestamp(1666666666)
        obj = State()
        self.assertEqual(obj.updated_at, test_date)

    def test_init_with_args_str(self):
        obj = State("some random string")
        self.assertTrue("some random string" not in obj.__dict__.values())

    def test_init_with_args_none(self):
        obj = State(None)
        self.assertTrue(None not in obj.__dict__.values())

    def test_name_type(self):
        self.assertEqual(str, type(State().name))

    def test_name_is_class_attribute(self):
        obj = State()
        self.assertTrue("name" not in obj.__dict__.keys())
        self.assertTrue("name" in dir(obj))

    def test_init_with_kwargs_id(self):
        obj_id = str(uuid.uuid4())
        obj = State(id=obj_id)
        self.assertEqual(obj.id, obj_id)

    def test_init_with_kwargs_created_at(self):
        date = datetime.today()
        obj = State(created_at=datetime.isoformat(date))
        self.assertEqual(obj.created_at, date)

    def test_init_with_kwargs_updated_at(self):
        date = datetime.today()
        obj = State(updated_at=datetime.isoformat(date))
        self.assertEqual(obj.updated_at, date)

    def test_init_with_kwargs_None_value(self):
        self.assertEqual(None, State(id=None).id)
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

    def test_init_with_multiple_kwargs(self):
        created_at = datetime.today()
        updated_at = datetime.today()
        obj_id = str(uuid.uuid4())
        obj = State(id=obj_id, created_at=datetime.isoformat(created_at),
                    updated_at=datetime.isoformat(updated_at))
        self.assertEqual(obj.id, obj_id)
        self.assertEqual(obj.created_at, created_at)
        self.assertEqual(obj.updated_at, updated_at)

    def test_init_with_args_and_kwargs(self):
        created_at = datetime.today()
        updated_at = datetime.today()
        obj_id = str(uuid.uuid4())
        obj = State(
            "some random string",
            id=obj_id,
            created_at=datetime.isoformat(created_at),
            updated_at=datetime.isoformat(updated_at))
        self.assertNotIn('some random string', obj.__dict__.values())
        self.assertEqual(obj.id, obj_id)
        self.assertEqual(obj.created_at, created_at)
        self.assertEqual(obj.updated_at, updated_at)

    def test_created_at_is_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_created_at_change(self):
        obj1 = State()
        sleep(0.01)
        obj2 = State()
        self.assertTrue(obj2.created_at > obj1.created_at)

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_updated_at_change(self):
        obj1 = State()
        sleep(0.01)
        obj2 = State()
        self.assertTrue(obj2.updated_at > obj1.updated_at)

    def test_object_uniqueness(self):
        self.assertNotEqual(State().id, State().id)


class TestStateStringRepresentation(unittest.TestCase):

    @patch('sys.stdout', io.StringIO())
    @patch('datetime.datetime', fake_datetime)
    @patch('uuid.uuid4', fake_uuid4)
    def test_str_rep_no_args(self):
        obj = State()
        print(obj, end="")
        fake_date = fake_datetime.today().__repr__()
        must_have = [
            "[State] (1)",
            "'id': '1'",
            "'created_at': {}".format(fake_date),
            "'updated_at': {}".format(fake_date)]
        stdout_value = sys.stdout.getvalue()

        for item in must_have:
            self.assertTrue(item in stdout_value)


class TestStateSave(unittest.TestCase):
    def test_save_changes_updated_at(self):
        obj = State()
        first_updated_at = obj.updated_at
        sleep(0.1)
        obj.save()
        self.assertTrue(obj.updated_at > first_updated_at)

    def test_save_store_obj_in_file(self):
        os.unlink('file.json')
        storage.reload()
        obj = State()
        obj.save()
        with open("file.json", "r", encoding="utf-8") as file:
            self.assertTrue("State.{}".format(obj.id) in file.read())
        pass

    def test_save_with_one_arg(self):
        obj = State()
        with self.assertRaises(TypeError):
            obj.save("some random string")


class TestStateToDict(unittest.TestCase):

    def test_to_dict_with_arg(self):
        obj = State()
        with self.assertRaises(TypeError):
            obj.to_dict("some random arg")

    @patch('uuid.uuid4', fake_uuid4)
    @patch('datetime.datetime', fake_datetime)
    def test_to_dict(self):
        obj = State()
        exp_dict = {
            'id': fake_uuid4(),
            '__class__': 'State',
            'created_at': fake_datetime.today().isoformat(),
            'updated_at': fake_datetime.today().isoformat()
        }
        self.assertDictEqual(obj.to_dict(), exp_dict)

    def test_to_dict_holds_the_right_values(self):
        obj = State()
        dict_rep = obj.to_dict()
        self.assertEqual(obj.id, dict_rep["id"])
        self.assertEqual("State", dict_rep["__class__"])
        self.assertEqual(datetime.isoformat(
            obj.created_at), dict_rep["created_at"])
        self.assertEqual(datetime.isoformat(
            obj.updated_at), dict_rep["updated_at"])

    def test_to_dict_hold_the_right_keys(self):
        obj = State()
        keys = obj.to_dict().keys()
        self.assertIn("updated_at", keys)
        self.assertIn("created_at", keys)
        self.assertIn("id", keys)
        self.assertIn("__class__", keys)

    def test_to_dict_value_are_of_right_type(self):
        obj = State()
        dict_rep = obj.to_dict()
        self.assertEqual(str, type(dict_rep["id"]))
        self.assertEqual(str, type(dict_rep["__class__"]))
        self.assertEqual(str, type(dict_rep["updated_at"]))
        self.assertEqual(str, type(dict_rep["created_at"]))

    def test_to_dict_contains_added_key(self):
        obj = State()
        obj.name = "Eletricity"
        self.assertIn("Eletricity", obj.to_dict().values())
        self.assertIn("name", obj.to_dict().keys())


if __name__ == "__main__":
    unittest.main()
