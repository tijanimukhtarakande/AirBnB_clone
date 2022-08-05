#!/usr/bin/python3
"""This module contains unittest code for the review module"""


import io
import os
import sys
from time import sleep
from unittest.mock import patch
from models.review import Review
import uuid
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


class TestReviewInit(unittest.TestCase):

    @patch('uuid.uuid4', fake_uuid4)
    def test_init_id(self):
        obj = Review()
        self.assertEqual(obj.id, "1")

    def test_init_add_to_storage(self):
        obj = Review()
        self.assertTrue(obj in storage.all().values())

    @patch('datetime.datetime', fake_datetime)
    def test_init_created_at(self):
        test_date = datetime.fromtimestamp(1666666666)
        obj = Review()
        self.assertEqual(obj.created_at, test_date)

    @patch('datetime.datetime', fake_datetime)
    def test_init_updated_at(self):
        test_date = datetime.fromtimestamp(1666666666)
        obj = Review()
        self.assertEqual(obj.updated_at, test_date)

    def test_init_with_args_str(self):
        obj = Review("some random string")
        self.assertTrue("some random string" not in obj.__dict__.values())

    def test_init_with_args_none(self):
        obj = Review(None)
        self.assertTrue(None not in obj.__dict__.values())

    def test_place_id_type(self):
        self.assertEqual(str, type(Review().place_id))

    def test_user_id_type(self):
        self.assertEqual(str, type(Review().user_id))

    def test_text_id_type(self):
        self.assertEqual(str, type(Review().text))

    def test_place_id_is_class_attribute(self):
        obj = Review()
        self.assertTrue("place_id" not in obj.__dict__.keys())
        self.assertTrue("place_id" in dir(obj))

    def test_user_id_is_class_attribute(self):
        obj = Review()
        self.assertTrue("user_id" not in obj.__dict__.keys())
        self.assertTrue("user_id" in dir(obj))

    def test_text_is_class_attribute(self):
        obj = Review()
        self.assertTrue("text" not in obj.__dict__.keys())
        self.assertTrue("text" in dir(obj))

    def test_init_with_kwargs_id(self):
        obj_id = str(uuid.uuid4())
        obj = Review(id=obj_id)
        self.assertEqual(obj.id, obj_id)

    def test_init_with_kwargs_created_at(self):
        date = datetime.today()
        obj = Review(created_at=datetime.isoformat(date))
        self.assertEqual(obj.created_at, date)

    def test_init_with_kwargs_updated_at(self):
        date = datetime.today()
        obj = Review(updated_at=datetime.isoformat(date))
        self.assertEqual(obj.updated_at, date)

    def test_init_with_kwargs_None_value(self):
        self.assertEqual(None, Review(id=None).id)
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

    def test_init_with_multiple_kwargs(self):
        created_at = datetime.today()
        updated_at = datetime.today()
        obj_id = str(uuid.uuid4())
        obj = Review(id=obj_id, created_at=datetime.isoformat(created_at),
                     updated_at=datetime.isoformat(updated_at))
        self.assertEqual(obj.id, obj_id)
        self.assertEqual(obj.created_at, created_at)
        self.assertEqual(obj.updated_at, updated_at)

    def test_init_with_args_and_kwargs(self):
        created_at = datetime.today()
        updated_at = datetime.today()
        obj_id = str(uuid.uuid4())
        obj = Review(
            "some random string",
            id=obj_id,
            created_at=datetime.isoformat(created_at),
            updated_at=datetime.isoformat(updated_at))
        self.assertNotIn('some random string', obj.__dict__.values())
        self.assertEqual(obj.id, obj_id)
        self.assertEqual(obj.created_at, created_at)
        self.assertEqual(obj.updated_at, updated_at)

    def test_created_at_is_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_created_at_change(self):
        obj1 = Review()
        sleep(0.01)
        obj2 = Review()
        self.assertTrue(obj2.created_at > obj1.created_at)

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_updated_at_change(self):
        obj1 = Review()
        sleep(0.01)
        obj2 = Review()
        self.assertTrue(obj2.updated_at > obj1.updated_at)

    def test_object_uniqueness(self):
        self.assertNotEqual(Review().id, Review().id)


class TestReviewStringRepresentation(unittest.TestCase):

    @patch('sys.stdout', io.StringIO())
    @patch('datetime.datetime', fake_datetime)
    @patch('uuid.uuid4', fake_uuid4)
    def test_str_rep_no_args(self):
        obj = Review()
        print(obj, end="")
        fake_date = fake_datetime.today().__repr__()
        must_have = [
            "[Review] (1)",
            "'id': '1'",
            "'created_at': {}".format(fake_date),
            "'updated_at': {}".format(fake_date)]
        stdout_value = sys.stdout.getvalue()

        for item in must_have:
            self.assertTrue(item in stdout_value)


class TestReviewSave(unittest.TestCase):
    def test_save_changes_updated_at(self):
        obj = Review()
        first_updated_at = obj.updated_at
        sleep(0.1)
        obj.save()
        self.assertTrue(obj.updated_at > first_updated_at)

    def test_save_store_obj_in_file(self):
        os.unlink('file.json')
        storage.reload()
        obj = Review()
        obj.save()
        with open("file.json", "r", encoding="utf-8") as file:
            self.assertTrue("Review.{}".format(obj.id) in file.read())
        pass

    def test_save_with_one_arg(self):
        obj = Review()
        with self.assertRaises(TypeError):
            obj.save("some random string")


class TestReviewToDict(unittest.TestCase):

    def test_to_dict_with_arg(self):
        obj = Review()
        with self.assertRaises(TypeError):
            obj.to_dict("some random arg")

    @patch('uuid.uuid4', fake_uuid4)
    @patch('datetime.datetime', fake_datetime)
    def test_to_dict(self):
        obj = Review()
        exp_dict = {
            'id': fake_uuid4(),
            '__class__': 'Review',
            'created_at': fake_datetime.today().isoformat(),
            'updated_at': fake_datetime.today().isoformat()
        }
        self.assertDictEqual(obj.to_dict(), exp_dict)

    def test_to_dict_holds_the_right_values(self):
        obj = Review()
        dict_rep = obj.to_dict()
        self.assertEqual(obj.id, dict_rep["id"])
        self.assertEqual("Review", dict_rep["__class__"])
        self.assertEqual(datetime.isoformat(
            obj.created_at), dict_rep["created_at"])
        self.assertEqual(datetime.isoformat(
            obj.updated_at), dict_rep["updated_at"])

    def test_to_dict_hold_the_right_keys(self):
        obj = Review()
        keys = obj.to_dict().keys()
        self.assertIn("updated_at", keys)
        self.assertIn("created_at", keys)
        self.assertIn("id", keys)
        self.assertIn("__class__", keys)

    def test_to_dict_value_are_of_right_type(self):
        obj = Review()
        dict_rep = obj.to_dict()
        self.assertEqual(str, type(dict_rep["id"]))
        self.assertEqual(str, type(dict_rep["__class__"]))
        self.assertEqual(str, type(dict_rep["updated_at"]))
        self.assertEqual(str, type(dict_rep["created_at"]))

    def test_to_dict_contains_added_key(self):
        obj = Review()
        obj.name = "Eletricity"
        self.assertIn("Eletricity", obj.to_dict().values())
        self.assertIn("name", obj.to_dict().keys())


if __name__ == "__main__":
    unittest.main()
