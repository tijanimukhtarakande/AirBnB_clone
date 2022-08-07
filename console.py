#!/usr/bin/python3
"""This module defines the HBNBCommand class that serves as an entry point
to the AirBnB console"""
import cmd
import os
import sys
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage

avaliable_classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review}


object_type = {
    "number_rooms": int,
    "number_bathrooms": int,
    "max_guest": int,
    "price_by_night": int,
    "latitude": float,
    "longitude": float,
    "age": int}


class HBNBCommand(cmd.Cmd):
    """Entry point to the command interpreter"""
    prompt = "(hbnb) "

    def do_clear(self, arg):
        """
        Usage: clear

        clears the screen
        """
        os.system('clear')

    def precmd(self, line: str):
        """
        precmd parses the line before it is executed by the available handlers

        :param line(str): is the user input
        :return (str): is the parsed line
        """
        line = line.strip()
        if re.search("[a-z]+\\.all\\(\\)$", line):
            class_name = line.split('.')[0]
            command = "all"
            return command + " " + class_name
        if re.search("[a-z]+\\.count\\(\\)$", line):
            class_name = line.split('.')[0]
            command = "count"
            return command + " " + class_name
        if re.search("[a-z]+\\.show\\(.*?\\)$", line):
            class_name = line.split('.')[0]
            command = "show"
            obj_id = line[line.find('(') + 1: -1]
            return command + " " + class_name + " " + obj_id
        if re.search("[a-z]+\\.destroy\\(.*?\\)$", line):
            class_name = line.split('.')[0]
            command = "destroy"
            obj_id = line[line.find('(') + 1: -1]
            return command + " " + class_name + " " + obj_id
        if re.search("[a-z]+\\.update\\(.*?\\)$", line):
            class_name = line.split('.')[0]
            command = "update"
            param = line[line.find('(') + 1: -1]
            try:
                update_dict = eval(param[param.find(',') + 1:])
                if type(update_dict) != dict:
                    raise TypeError
            except BaseException:
                param = param.replace(',', '', 2)
                return command + " " + class_name + " " + param
            obj_id = param[0: param.find(',')].strip('" ')
            if class_name not in avaliable_classes.keys():
                print("** class doesn't exist **")
                return ""
            all_objs = storage.all()
            obj_name = "{}.{}".format(class_name, obj_id)
            obj = all_objs.get(obj_name, None)
            if obj is None:
                print("** no instance found **")
                return ""
            for key, val in update_dict.items():
                setattr(obj, key, object_type.get(key, str)(val))
            obj.save()
            return ""
        return line

    def do_count(self, arg):
        """
        Usage: count <class_name> or <class_name>.count()

        it returns the number of objects of the type <class_name>
        """
        arg = split(arg)
        if arg[0] not in avaliable_classes.keys():
            return print("** class doesn't exist **")
        objs = storage.all()
        count = 0
        for key in objs:
            if arg[0] == objs[key].__class__.__name__:
                count += 1
        print(count)

    def do_quit(self, arg: str):
        """Quit command to exit the program"""
        sys.exit()

    def do_EOF(self, arg):
        """Quits the program when EOF is reached"""
        sys.exit()

    def do_create(self, arg):
        """
        Usage: create <class_name>

        Creates a new object of type <class_name>
        """
        arg = split(arg)
        if len(arg) < 1:
            return print("** class name missing **")
        if arg[0] not in avaliable_classes.keys():
            return print("** class doesn't exist **")
        new_obj = avaliable_classes[arg[0]]()
        storage.save()
        print(new_obj.id)

    def do_show(self, arg):
        """
        Usage : show <class_name> <object_id> or <class_name>.show(<object_id>)

        Displays the details of the given object_id
        """
        arg = split(arg)
        if len(arg) < 1:
            return print("** class name missing **")
        if arg[0] not in avaliable_classes.keys():
            return print("** class doesn't exist **")
        if len(arg) < 2:
            return print("** instance id missing **")
        all_objs = storage.all()
        obj_name = "{}.{}".format(arg[0], arg[1])
        obj = all_objs.get(obj_name, None)
        if obj is None:
            return print("** no instance found **")
        print(obj)

    def do_all(self, arg):
        """
        Usage: all or all <class_name> or <class_name>.all()

        Display all objects if no class_name is specified else it displays
        all objects of type class_name
        """
        all_objs = storage.all()
        to_print = []
        arg = split(arg)
        if len(arg) > 0:
            if arg[0] not in avaliable_classes.keys():
                return print("** class doesn't exist **")
            for key in all_objs:
                if key.split('.')[0] == arg[0]:
                    to_print.append(all_objs[key].__str__())
            print(to_print)
            return
        for key in all_objs:
            to_print.append(all_objs[key].__str__())
        print(to_print)

    def do_destroy(self, arg):
        """
        Usage: destroy <class_name> <object_id> or \
<class_name>.destroy(<object_id>)

        Removes an object with the given class_name and object_id from storage
        """
        arg = split(arg)
        if len(arg) < 1:
            return print("** class name missing **")
        if arg[0] not in avaliable_classes.keys():
            return print("** class doesn't exist **")
        if len(arg) < 2:
            return print("** instance id missing **")
        all_objs = storage.all()
        obj_name = "{}.{}".format(arg[0], arg[1])
        if all_objs.pop(obj_name, None) is None:
            return print("** no instance found **")
        storage.save()

    def do_update(self, arg):
        """
        Usage: update <class name> <id> <attribute name> "<attribute value>"
or <class name>.update(<id>, <attribute name>, <attribute value>)
or <class name>.update(<id>, <dictionary representation>)

        Updates the details of the given id with the given attribute name and
        value or dictionary representation
        """
        arg = split(arg)
        if len(arg) < 1:
            return print("** class name missing **")
        if arg[0] not in avaliable_classes.keys():
            return print("** class doesn't exist **")
        if len(arg) < 2:
            return print("** instance id missing **")
        all_objs = storage.all()
        obj_name = "{}.{}".format(arg[0], arg[1])
        obj = all_objs.get(obj_name, None)
        if obj is None:
            return print("** no instance found **")
        if len(arg) < 3:
            return print("** attribute name missing **")
        if len(arg) < 4:
            return print("** value missing **")
        setattr(obj, arg[2], object_type.get(arg[2], str)(arg[3]))
        obj.save()

    def emptyline(self):
        pass


def split(arg: str, delim=' '):
    """
    split seperates a string using the delim paramerter as the seperator

    :param arg(str): is the string to be seperated
    :param delim(str): is the character to be used as the seperator
    :return (list[str]): is a list of string
    """
    split_val = []
    buff = ""
    temp = None
    for i in arg:
        if i == delim:
            if temp is None:
                buff and split_val.append(buff)
                buff = ""
            else:
                temp += i
        elif i == '"':
            if temp is None:
                temp = ""
            else:
                buff += temp
                temp = None
        else:
            if temp is None:
                buff += i
            else:
                temp += i
    if buff:
        split_val.append(buff)
    return split_val


if __name__ == '__main__':
    HBNBCommand().cmdloop()
