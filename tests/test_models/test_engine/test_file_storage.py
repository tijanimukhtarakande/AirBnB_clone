#!/usr/bin/python3
"""This module contains unittest code for the file_storage module"""

import models
import os
import json
from datetime import datetime
from models.engine.file_storage import FileStorage
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel
from models.state import State
import unittest


class TestFileStorageInit(unittest.TestCase):
    def test_file_storage_private__file_path(self):
        storage = FileStorage()
        self.assertNotIn("__file_path", storage.__dict__)
        self.assertNotIn("__file_path", dir(storage))
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_file_storage_private__objects(self):
        storage = FileStorage()
        self.assertNotIn("__objects", storage.__dict__)
        self.assertNotIn("__objects", dir(storage))
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_file_strorage_init(self):
        self.assertEqual(FileStorage, type(models.storage))
        self.assertEqual(FileStorage, type(FileStorage()))

    def test_file_storage_init_with_args(self):
        with self.assertRaises(TypeError):
            FileStorage("some random arg")


class TestFileStorageSave(unittest.TestCase):

    def setUp(self):
        models.storage.all().clear()
        try:
            os.remove("file.json")
        except BaseException:
            pass

    def test_all_return_type(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_call_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all("some random arg")

    def test_call_new_with_two_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), "some random arg")

    def test_call_new_with_invalid_object(self):
        with self.assertRaises(AttributeError):
            models.storage.new("some object with no id attribute")

    def test_call_new_with_None(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_call_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_new(self):
        basemodel = BaseModel()
        state = State()
        user = User()
        city = City()
        review = Review()
        place = Place()
        amenity = Amenity()

        self.assertTrue("BaseModel.{}".format(basemodel.id)
                        in models.storage.all().keys())
        self.assertTrue(basemodel
                        in models.storage.all().values())

        self.assertTrue("State.{}".format(state.id)
                        in models.storage.all().keys())
        self.assertTrue(state
                        in models.storage.all().values())

        self.assertTrue("User.{}".format(user.id)
                        in models.storage.all().keys())
        self.assertTrue(user
                        in models.storage.all().values())

        self.assertTrue("City.{}".format(city.id)
                        in models.storage.all().keys())
        self.assertTrue(city
                        in models.storage.all().values())

        self.assertTrue("Review.{}".format(review.id)
                        in models.storage.all().keys())
        self.assertTrue(review
                        in models.storage.all().values())

        self.assertTrue("Place.{}".format(place.id)
                        in models.storage.all().keys())
        self.assertTrue(place
                        in models.storage.all().values())

        self.assertTrue("Amenity.{}".format(amenity.id)
                        in models.storage.all().keys())
        self.assertTrue(amenity
                        in models.storage.all().values())

    def test_save(self):
        basemodel = BaseModel()
        state = State()
        user = User()
        city = City()
        review = Review()
        place = Place()
        amenity = Amenity()

        models.storage.save()

        with open("file.json", "r", encoding="utf-8") as file:
            content = file.read()
            self.assertTrue("BaseModel.{}".format(basemodel.id)
                            in content)

            self.assertTrue("State.{}".format(state.id)
                            in content)

            self.assertTrue("User.{}".format(user.id)
                            in content)

            self.assertTrue("City.{}".format(city.id)
                            in content)

            self.assertTrue("Review.{}".format(review.id)
                            in content)

            self.assertTrue("Place.{}".format(place.id)
                            in content)

            self.assertTrue("Amenity.{}".format(amenity.id)
                            in content)

    def test_reload(self):
        basemodel = BaseModel()
        state = State()
        user = User()
        city = City()
        review = Review()
        place = Place()
        amenity = Amenity()
        models.storage.save()
        models.storage.all().clear()
        self.assertDictEqual({}, models.storage.all())
        models.storage.reload()
        content = models.storage.all().keys()
        self.assertTrue("BaseModel.{}".format(basemodel.id)
                        in content)

        self.assertTrue("State.{}".format(state.id)
                        in content)

        self.assertTrue("User.{}".format(user.id)
                        in content)

        self.assertTrue("City.{}".format(city.id)
                        in content)

        self.assertTrue("Review.{}".format(review.id)
                        in content)

        self.assertTrue("Place.{}".format(place.id)
                        in content)

        self.assertTrue("Amenity.{}".format(amenity.id)
                        in content)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload("some random arg")

    def test_reload_no_file(self):
        with self.assertRaises(IOError):
            open("file.json")
            models.storage.reload()
            self.assertDictEqual({}, models.storage.all())


if __name__ == "__main__":
    unittest.main()
