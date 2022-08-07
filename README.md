# **AirBnB clone**

## **The Console Overview**

The console marks the beginning of the ALX AirBnb Project.
It entails creating a command line interface to manage objects and a file storage engine to persist them to disk. The file storage is temporary and it would be later moved to a database.

<br>

## **Object Types**

In the table below you will find all the classes of objects that can be created and attributes that exists on them. The [BaseModel](/models/base_model.py) is inherited by the other classes, it provides timestamps, ids, and access to the file storage.

| Class                              | Public class attrubutes                                                                                                                                | Public instance attributes       | Methods               |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- | --------------------- |
| [BaseModel](/models/base_model.py) | \_                                                                                                                                                     | `id`, `created_at`, `updated_at` | `save()`, `to_dict()` |
| [User](/models/user.py)            | `email`, `password`, `first_name`, `last_name`                                                                                                         | -                                | -                     |
| [State](/models/state.py)          | `name`                                                                                                                                                 | -                                | -                     |
| [City](/models/city.py)            | `state_id`, `name`                                                                                                                                     | -                                | -                     |
| [Amenity](/models/amenity.py)      | `name`                                                                                                                                                 | -                                | -                     |
| [Place](/models/place.py)          | `city_id`, `user_id`, `name`, `description`, `number_rooms`, `number_bathrooms`, `max_guest`, `price_by_night`, `latitude`, `longitude`, `amenity_ids` | -                                | -                     |
| [Review](/models/review.py)        | `place_d`, `user_id`, `text`                                                                                                                           | -                                | -                     |

<br>

- [`to_dict()`](/models/base_model.py): The `to_dict()` function returns a dictionary of attributes names and their respective values.
- [`save()`](/models/base_model.py): A call to this function set the `updated_at` attribute to the current time and persists the current state of the object to the file storage.

Ids are generated using the uuid4 module and the datetime library for the `updated_at` and `created_at` attributes.

<br>

## **The File Storage engine**

The [file_storage](/models/engine/file_storage.py) module provides the FileStorage class that enables us persist the state of objects to the disk.
It contains the follow attribures and methods:

- `__file_path`: A private class attribute that holds the path to the storage file.
- `__objects`: A dict object that temporarily holds the current state of all objects in memory before they are saved. It is a private class attribute and can only be accessed through a call to the `all()`.
- `all()`: Takes no argument and returns a reference to the private `__objects` dict.
- `new(obj)`: Takes in one object of type from available classes and creates an entry for it in the `objects` dict. The entry has a key that is represented like so `<class_name>.<id>` eg, `BaseModel.31923923-213123-1232-1123`.
- `save()`: Stores a Json representation of the `__objects` dict to the file named `__file_path`.
- `reload()`: Restores the state of all objects from `__file_path` and stores it in the `__objects` dict.

<br>

An intstance of the FileStorage class resides in the [model module](/models/__init__.py). It is the only instance used and created throughout the whole program. The `reload()` is also called right after the instantiation to restore the objects.

<br>

## **The console**

The [console module](/console.py) lays out a neat and user friendly interface to interact with the application. It provides functionalities that allows for creating, deleting, updating and viewing objects.

To start the console, run the command below in the root directory of the project, You might need to run `chmod u+x` to provide execution permission for the `console.py` file.

```shell
➜  AirBnB_clone git:(main) ✗ chmod u+x console.py ; ./console.py
(hbnb)
```

<br>

Using the `help` command you get the documentation of all the commands baked into the console, `help <command_name>` or `? <command_name>` gives the documentation of the command if present. To exit the CLI use the `quit` command.

```shel
➜  AirBnB_clone git:(main) ✗ ./console.py
(hbnb) help
Documented commands (type help <topic>):
========================================
EOF  all  clear  count  create  destroy  help  quit  show  update
(hbnb) help update
Usage: update <class name> <id> <attribute name> "<attribute value>"
   or <class name>.update(<id>, <attribute name>, <attribute value>)
   or <class name>.update(<id>, <dictionary representation>)

Updates the details of the given id with the given attribute name and value or dictionary representation
(hbnb) quit
➜  AirBnB_clone git:(main)
```

<br>

### **Command List**

Brief enumeration of the available commands, what they do and how to use them.

- `create` : For creations of objects, use the create command. It takes in a single argument which is the class name of the object to be created. The class name must valid an part of the available classes [here](/console.py). The id of the newly created object is printed out if the operation was successful.

```
Usage:
   create <class_name>
```

```shell
(hbnb) create InvalidClassName
** class doesn't exist **
(hbnb) create User
4c65bf4a-7658-4910-b522-5fb92451694f
```

<br>

- `show` : Takes in two arguments, `class_name` and `id`, if any object matches it is printed out.

```
Usage:
   show <class_name> <id>
   <class_name>.show(<id>)
```

```shell
(hbnb) show User 4c65bf4a-7658-4910-b522-5fb92451694f
[User] (4c65bf4a-7658-4910-b522-5fb92451694f) {'id': '4c65bf4a-7658-4910-b522-5fb92451694f', 'created_at': datetime.datetime(2022, 8, 5, 15, 8, 24, 978638), 'updated_at': datetime.datetime(2022, 8, 5, 15, 8, 24, 978638)}
(hbnb)
(hbnb)
(hbnb) User.show("4c65bf4a-7658-4910-b522-5fb92451694f")
[User] (4c65bf4a-7658-4910-b522-5fb92451694f) {'id': '4c65bf4a-7658-4910-b522-5fb92451694f', 'created_at': datetime.datetime(2022, 8, 5, 15, 8, 24, 978638), 'updated_at': datetime.datetime(2022, 8, 5, 15, 8, 24, 978638)}
```

<br>

- `destroy` : Takes in two arguments, `class_name` and `id`, if any object matches it is removed from the file storage.

```
Usage:
   destroy <class_name> <id>
   <class_name>.destroy(<id>)
```

```shell
(hbnb) User.show("4c65bf4a-7658-4910-b522-5fb92451694f")
[User] (4c65bf4a-7658-4910-b522-5fb92451694f) {'id': '4c65bf4a-7658-4910-b522-5fb92451694f', 'created_at': datetime.datetime(2022, 8, 5, 15, 8, 24, 978638), 'updated_at': datetime.datetime(2022, 8, 5, 15, 8, 24, 978638)}
(hbnb)
(hbnb) User.destroy("4c65bf4a-7658-4910-b522-5fb92451694f")
(hbnb)
(hbnb) User.show("4c65bf4a-7658-4910-b522-5fb92451694f")
** no instance found **
```

<br>

- `all` : Prints all string representation of all instances based or not on the class name.

```
Usage:
   all
   all <class_name>
   <class_name>.all()
```

```shell
(hbnb) create User
02a33dd5-1876-4f78-bd53-492d555608a3
(hbnb)
(hbnb) create Place
02d36bbc-1e0b-4a2a-ba35-2c6553aee88a
(hbnb)
(hbnb) all
["[User] (02a33dd5-1876-4f78-bd53-492d555608a3) {'id': '02a33dd5-1876-4f78-bd53-492d555608a3', 'created_at': datetime.datetime(2022, 8, 5, 15, 30, 44, 374698), 'updated_at': datetime.datetime(2022, 8, 5, 15, 30, 44, 374698)}", "[Place] (02d36bbc-1e0b-4a2a-ba35-2c6553aee88a) {'id': '02d36bbc-1e0b-4a2a-ba35-2c6553aee88a', 'created_at': datetime.datetime(2022, 8, 5, 15, 30, 54, 576713), 'updated_at': datetime.datetime(2022, 8, 5, 15, 30, 54, 576713)}"]
(hbnb)
(hbnb) all User
["[User] (02a33dd5-1876-4f78-bd53-492d555608a3) {'id': '02a33dd5-1876-4f78-bd53-492d555608a3', 'created_at': datetime.datetime(2022, 8, 5, 15, 30, 44, 374698), 'updated_at': datetime.datetime(2022, 8, 5, 15, 30, 44, 374698)}"]
(hbnb)
(hbnb) Place.all()
["[Place] (02d36bbc-1e0b-4a2a-ba35-2c6553aee88a) {'id': '02d36bbc-1e0b-4a2a-ba35-2c6553aee88a', 'created_at': datetime.datetime(2022, 8, 5, 15, 30, 54, 576713), 'updated_at': datetime.datetime(2022, 8, 5, 15, 30, 54, 576713)}"]
```

<br>

- `count` : Prints the number of instance of the given class present in the file storage.

```
Usage:
   count <class_name>
   <class_name>.count()
```

```shell
(hbnb) State.count()
0
(hbnb) create State
305d392d-129e-4e70-b3fa-b98684a58967
(hbnb)
(hbnb) create State
544110cd-a0c5-4fdf-b128-dfa441f0bea3
(hbnb) State.count()
2
```

<br>

- `update` : Prints the number of instance of the given class present in the file storage.

```
Usage:
   <class name> <id> <attribute name> "<attribute value>"
   <class name>.update(<id>, <attribute name>, <attribute value>)
   <class name>.update(<id>, <dictionary representation>)
```

```shell
(hbnb) User.show("e6d3cef6-a493-404e-bdef-c47b9afdae93")
[User] (e6d3cef6-a493-404e-bdef-c47b9afdae93) {'id': 'e6d3cef6-a493-404e-bdef-c47b9afdae93', 'created_at': datetime.datetime(2022, 8, 5, 15, 44, 38, 434537), 'updated_at': datetime.datetime(2022, 8, 5, 15, 44, 38, 434537)}
(hbnb)
(hbnb) User.update("e6d3cef6-a493-404e-bdef-c47b9afdae93", "first_name", "some_name")
(hbnb) update User "e6d3cef6-a493-404e-bdef-c47b9afdae93" "last_name" "some_name"
(hbnb) User.update("e6d3cef6-a493-404e-bdef-c47b9afdae93", {'email': "some_mail@mail.com", 'password': 'some_password'})
(hbnb)
(hbnb) User.show("e6d3cef6-a493-404e-bdef-c47b9afdae93")
[User] (e6d3cef6-a493-404e-bdef-c47b9afdae93) {'id': 'e6d3cef6-a493-404e-bdef-c47b9afdae93', 'created_at': datetime.datetime(2022, 8, 5, 15, 44, 38, 434537), 'updated_at': datetime.datetime(2022, 8, 5, 15, 47, 20, 84458), 'first_name': 'some_name', 'last_name': 'some_name', 'email': 'some_mail@mail.com', 'password': 'some_password'}
```

<br>

- `clear` : Clears the screen.

```
Usage:
   clear
```

<br>

## **Tests**

All modules are tested, you can find the unittest code in the [tests](/tests) folder.
To start the test run the code below.

```bash
➜  AirBnB_clone git:(main) ✗ python3 -m unittest discover tests
.....................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 245 tests in 1.938s

OK
```

<br>

## **Authors**

List of individuals having contributed to the repository.

- Michael Adewole - <[michaseyi](github.com/michaeyi@gmail.com)>
- Tijani Mukhtar - <[Tiganimukhtarakande](github.com/Tiganimukhtarakande)>
