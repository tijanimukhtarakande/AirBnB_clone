#!/usr/bin/python
"""This module contains unittest code for the console module"""

import unittest
import sys
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
import os
from models import storage
from models.engine.file_storage import FileStorage


class TestConsolePrompt(unittest.TestCase):

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    @patch('sys.stdout', new=StringIO())
    def test_empty_line(self):
        self.assertFalse(HBNBCommand().onecmd(""))
        self.assertEqual("", sys.stdout.getvalue())


class TestConsoleHelp(unittest.TestCase):

    @patch('sys.stdout', new=StringIO())
    def test_EOF(self):
        output = """Quits the program when EOF is reached\n"""
        self.assertFalse(HBNBCommand().onecmd("help EOF"))
        self.assertEqual(output, sys.stdout.getvalue())

    @patch('sys.stdout', new=StringIO())
    def test_all(self):
        output = """
        Usage: all or all <class_name> or <class_name>.all()

        Display all objects if no class_name is specified else it displays
        all objects of type class_name
        \n"""
        self.assertFalse(HBNBCommand().onecmd("help all"))
        self.assertEqual(output, sys.stdout.getvalue())

    @patch('sys.stdout', new=StringIO())
    def test_count(self):
        output = """
        Usage: count <class_name> or <class_name>.count()

        it returns the number of objects of the type <class_name>
        \n"""
        self.assertFalse(HBNBCommand().onecmd("help count"))
        self.assertEqual(output, sys.stdout.getvalue())

    @patch('sys.stdout', new=StringIO())
    def test_create(self):
        output = """
        Usage: create <class_name>

        Creates a new object of type <class_name>
        \n"""
        self.assertFalse(HBNBCommand().onecmd("help create"))
        self.assertEqual(output, sys.stdout.getvalue())

    @patch('sys.stdout', new=StringIO())
    def test_destroy(self):
        output = """
        Usage: destroy <class_name> <object_id> or \
<class_name>.destroy(<object_id>)

        Removes an object with the given class_name and object_id from storage
        \n"""
        self.assertFalse(HBNBCommand().onecmd("help destroy"))
        self.assertEqual(output, sys.stdout.getvalue())

    @patch('sys.stdout', new=StringIO())
    def test_help(self):
        output = """List available commands with "help" or detailed help \
with "help cmd".\n"""
        self.assertFalse(HBNBCommand().onecmd("help help"))
        self.assertEqual(output, sys.stdout.getvalue())

    @patch('sys.stdout', new=StringIO())
    def test_quit(self):
        output = """Quit command to exit the program\n"""
        self.assertFalse(HBNBCommand().onecmd("help quit"))
        self.assertEqual(output, sys.stdout.getvalue())

    @patch('sys.stdout', new=StringIO())
    def test_show(self):
        output = """
        Usage : show <class_name> <object_id> or <class_name>.show(<object_id>)

        Displays the details of the given object_id
        \n"""
        self.assertFalse(HBNBCommand().onecmd("help show"))
        self.assertEqual(output, sys.stdout.getvalue())

    @patch('sys.stdout', new=StringIO())
    def test_update(self):
        output = """
        Usage: update <class name> <id> <attribute name> "<attribute value>"
or <class name>.update(<id>, <attribute name>, <attribute value>)
or <class name>.update(<id>, <dictionary representation>)

        Updates the details of the given id with the given attribute name and
        value or dictionary representation
        \n"""
        self.assertFalse(HBNBCommand().onecmd("help update"))
        self.assertEqual(output, sys.stdout.getvalue())
