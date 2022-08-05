#!/usr/bin/python3
"""This module contains unittest code for the place module"""


import io
import os
import sys
from time import sleep
from unittest.mock import patch
import uuid
from models.place import Place
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


class TestPlaceInit(unittest.TestCase):
    def setUp(self):
        try:
            os.remove("file.json")
        except BaseException:
            pass
        storage.all().clear()
        storage.save()

    @patch('uuid.uuid4', fake_uuid4)
    def test_init_id(self):
        obj = Place()
        self.assertEqual(obj.id, "1")

    def test_init_add_to_storage(self):
        obj = Place()
        self.assertTrue(obj in storage.all().values())

    @patch('datetime.datetime', fake_datetime)
    def test_init_created_at(self):
        test_date = datetime.fromtimestamp(1666666666)
        obj = Place()
        self.assertEqual(obj.created_at, test_date)

    @patch('datetime.datetime', fake_datetime)
    def test_init_updated_at(self):
        test_date = datetime.fromtimestamp(1666666666)
        obj = Place()
        self.assertEqual(obj.updated_at, test_date)

    def test_init_with_args_str(self):
        obj = Place("some random string")
        self.assertTrue("some random string" not in obj.__dict__.values())

    def test_init_with_args_none(self):
        obj = Place(None)
        self.assertTrue(None not in obj.__dict__.values())

    def test_name_type(self):
        self.assertEqual(str, type(Place().name))

    def test_city_id_type(self):
        self.assertEqual(str, type(Place().city_id))

    def test_user_id_type(self):
        self.assertEqual(str, type(Place().user_id))

    def test_description_type(self):
        self.assertEqual(str, type(Place().description))

    def test_number_rooms_type(self):
        self.assertEqual(int, type(Place().number_rooms))

    def test_number_bathrooms_type(self):
        self.assertEqual(int, type(Place().number_bathrooms))

    def test_max_guest_type(self):
        self.assertEqual(int, type(Place().max_guest))

    def test_price_by_night_type(self):
        self.assertEqual(int, type(Place().price_by_night))

    def test_latitude_type(self):
        self.assertEqual(float, type(Place().latitude))

    def test_longitude_type(self):
        self.assertEqual(float, type(Place().longitude))

    def test_amenity_ids_type(self):
        self.assertEqual(list, type(Place().amenity_ids))

    def test_name_is_class_attribute(self):
        obj = Place()
        self.assertTrue("name" not in obj.__dict__.keys())
        self.assertTrue("name" in dir(obj))

    def test_city_id_is_class_attribute(self):
        obj = Place()
        self.assertTrue("city_id" not in obj.__dict__.keys())
        self.assertTrue("city_id" in dir(obj))

    def test_user_id_is_class_attribute(self):
        obj = Place()
        self.assertTrue("user_id" not in obj.__dict__.keys())
        self.assertTrue("user_id" in dir(obj))

    def test_description_is_class_attribute(self):
        obj = Place()
        self.assertTrue("description" not in obj.__dict__.keys())
        self.assertTrue("description" in dir(obj))

    def test_number_rooms_is_class_attribute(self):
        obj = Place()
        self.assertTrue("number_rooms" not in obj.__dict__.keys())
        self.assertTrue("number_rooms" in dir(obj))

    def test_number_bathrooms_is_class_attribute(self):
        obj = Place()
        self.assertTrue("number_bathrooms" not in obj.__dict__.keys())
        self.assertTrue("number_bathrooms" in dir(obj))

    def test_max_guest_is_class_attribute(self):
        obj = Place()
        self.assertTrue("max_guest" not in obj.__dict__.keys())
        self.assertTrue("max_guest" in dir(obj))

    def test_price_by_night_is_class_attribute(self):
        obj = Place()
        self.assertTrue("price_by_night" not in obj.__dict__.keys())
        self.assertTrue("price_by_night" in dir(obj))

    def test_latitude_is_class_attribute(self):
        obj = Place()
        self.assertTrue("latitude" not in obj.__dict__.keys())
        self.assertTrue("latitude" in dir(obj))

    def test_longitude_is_class_attribute(self):
        obj = Place()
        self.assertTrue("longitude" not in obj.__dict__.keys())
        self.assertTrue("longitude" in dir(obj))

    def test_amenity_ids_is_class_attribute(self):
        obj = Place()
        self.assertTrue("amenity_ids" not in obj.__dict__.keys())
        self.assertTrue("amenity_ids" in dir(obj))

    def test_init_with_kwargs_id(self):
        obj_id = str(uuid.uuid4())
        obj = Place(id=obj_id)
        self.assertEqual(obj.id, obj_id)

    def test_init_with_kwargs_created_at(self):
        date = datetime.today()
        obj = Place(created_at=datetime.isoformat(date))
        self.assertEqual(obj.created_at, date)

    def test_init_with_kwargs_updated_at(self):
        date = datetime.today()
        obj = Place(updated_at=datetime.isoformat(date))
        self.assertEqual(obj.updated_at, date)

    def test_init_with_kwargs_None_value(self):
        self.assertEqual(None, Place(id=None).id)
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)

    def test_init_with_multiple_kwargs(self):
        created_at = datetime.today()
        updated_at = datetime.today()
        obj_id = str(uuid.uuid4())
        obj = Place(id=obj_id, created_at=datetime.isoformat(created_at),
                    updated_at=datetime.isoformat(updated_at))
        self.assertEqual(obj.id, obj_id)
        self.assertEqual(obj.created_at, created_at)
        self.assertEqual(obj.updated_at, updated_at)

    def test_init_with_args_and_kwargs(self):
        created_at = datetime.today()
        updated_at = datetime.today()
        obj_id = str(uuid.uuid4())
        obj = Place(
            "some random string",
            id=obj_id,
            created_at=datetime.isoformat(created_at),
            updated_at=datetime.isoformat(updated_at))
        self.assertNotIn('some random string', obj.__dict__.values())
        self.assertEqual(obj.id, obj_id)
        self.assertEqual(obj.created_at, created_at)
        self.assertEqual(obj.updated_at, updated_at)

    def test_created_at_is_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_created_at_change(self):
        obj1 = Place()
        sleep(0.01)
        obj2 = Place()
        self.assertTrue(obj2.created_at > obj1.created_at)

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_updated_at_change(self):
        obj1 = Place()
        sleep(0.01)
        obj2 = Place()
        self.assertTrue(obj2.updated_at > obj1.updated_at)

    def test_object_uniqueness(self):
        self.assertNotEqual(Place().id, Place().id)


class TestPlaceStringRepresentation(unittest.TestCase):
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
        obj = Place()
        print(obj, end="")
        fake_date = fake_datetime.today().__repr__()
        must_have = [
            "[Place] (1)",
            "'id': '1'",
            "'created_at': {}".format(fake_date),
            "'updated_at': {}".format(fake_date)]
        stdout_value = sys.stdout.getvalue()

        for item in must_have:
            self.assertTrue(item in stdout_value)


class TestPlaceSave(unittest.TestCase):
    def setUp(self):
        try:
            os.remove("file.json")
        except BaseException:
            pass
        storage.all().clear()
        storage.save()

    def test_save_changes_updated_at(self):
        obj = Place()
        first_updated_at = obj.updated_at
        sleep(0.1)
        obj.save()
        self.assertTrue(obj.updated_at > first_updated_at)

    def test_save_store_obj_in_file(self):
        os.unlink('file.json')
        storage.reload()
        obj = Place()
        obj.save()
        with open("file.json", "r", encoding="utf-8") as file:
            self.assertTrue("Place.{}".format(obj.id) in file.read())
        pass

    def test_save_with_one_arg(self):
        obj = Place()
        with self.assertRaises(TypeError):
            obj.save("some random string")


class TestPlaceToDict(unittest.TestCase):

    def setUp(self):
        try:
            os.remove("file.json")
        except BaseException:
            pass
        storage.all().clear()
        storage.save()

    def test_to_dict_with_arg(self):
        obj = Place()
        with self.assertRaises(TypeError):
            obj.to_dict("some random arg")

    @patch('uuid.uuid4', fake_uuid4)
    @patch('datetime.datetime', fake_datetime)
    def test_to_dict(self):
        obj = Place()
        exp_dict = {
            'id': fake_uuid4(),
            '__class__': 'Place',
            'created_at': fake_datetime.today().isoformat(),
            'updated_at': fake_datetime.today().isoformat()
        }
        self.assertDictEqual(obj.to_dict(), exp_dict)

    def test_to_dict_holds_the_right_values(self):
        obj = Place()
        dict_rep = obj.to_dict()
        self.assertEqual(obj.id, dict_rep["id"])
        self.assertEqual("Place", dict_rep["__class__"])
        self.assertEqual(datetime.isoformat(
            obj.created_at), dict_rep["created_at"])
        self.assertEqual(datetime.isoformat(
            obj.updated_at), dict_rep["updated_at"])

    def test_to_dict_hold_the_right_keys(self):
        obj = Place()
        keys = obj.to_dict().keys()
        self.assertIn("updated_at", keys)
        self.assertIn("created_at", keys)
        self.assertIn("id", keys)
        self.assertIn("__class__", keys)

    def test_to_dict_value_are_of_right_type(self):
        obj = Place()
        dict_rep = obj.to_dict()
        self.assertEqual(str, type(dict_rep["id"]))
        self.assertEqual(str, type(dict_rep["__class__"]))
        self.assertEqual(str, type(dict_rep["updated_at"]))
        self.assertEqual(str, type(dict_rep["created_at"]))

    def test_to_dict_contains_added_key(self):
        obj = Place()
        obj.name = "Eletricity"
        self.assertIn("Eletricity", obj.to_dict().values())
        self.assertIn("name", obj.to_dict().keys())


if __name__ == "__main__":
    unittest.main()
