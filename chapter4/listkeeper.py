#!/usr/bin/env python3

import os

YES = frozenset({"y", "Y", "yes", "Yes", "YES"})  # frozonset, a set that once created, cannot be changed


def main():
    dirty = False  # flag of list unsaved
    items = []

    filename, items = choose_file()  ## thought
    if not filename:  # if filename is None
        print("Cancelled")
        return

    while True:
        print("\nList keeeper\n")
        print_list(items)  ## thought
        choice = get_choice(items, dirty)  ## thought

        if choice in "Aa":
            dirty = add_item(items, dirty)  ## thought
        elif choice in "Dd":
            dirty = delete_item(items, dirty)  ## thought
        elif choice in "Ss":
            dirty = save_list(filename, items)  ## thought
        elif choice in "Qq":
            if (dirty and (get_string("Save unsaved changes (y/n)", "yes/no", "y") in YES)):  ## thought
                save_list(filename, items, True)  ## thought
            break


def choose_file():
    enter_filename = False
    print("\nList Keeper\n")
    files = [x for x in os.listdir(".") if
             x.endswith(".lst")]  # list comprehension, get all files in the currrent directory
    if not files:
        enter_filename = True
    if not enter_filename:
        print_list(files)  ## function
        index = get_integer("Specify file's number (or 0 to create a new one)", "number", maximum=len(files),
                            allow_zero=True)  ## function, because of this case, there is a enter_filename label
        if index == 0:
            enter_filename = True
        else:
            filename = files[index - 1]
            items = load_list(filename)  ## function
    if enter_filename:
        filename = get_string("Choose filename", "filename")  ## function
        if not filename.endswith(".lst"):
            filename += ".lst"
        items = []
    return filename, items


def print_list(items):
    if not items:
        print("-- no items are in the list --")
    else:
        width = 1 if len(items) < 10 else 2 if len(
            items) < 100 else 3  # embedded conditional comprehension, digit format requirement
        for i, item in enumerate(items):  # enumerate, add a indexer
            print("{0:{width}}: {item}".format(i + 1, **locals()))  # start from 1, format with mapping unpacking
    print()  # a new blank line


# the choice is different according to the current state
def get_choice(items, dirty):
    while True:
        if items:
            if dirty:  # not saved
                menu = "[A]dd [D]elete [S]ave [Q]uit"
                valid_choices = "AaDdSsQq"
            else:
                menu = "[A]dd [D]elete [Q]uit"
                valid_choices = "AaDdQq"
        else:
            menu = "[A]dd [Q]uit"
            valid_choices = "AaQq"

        choice = get_string(menu, "choice", "a")  ## function

        if choice not in valid_choices:
            print("ERROR: invalid choice -- enter one of '{0}'".format(valid_choices))
            print("Press Enter to continue...")
        else:
            return choice


def add_item(items, dirty):
    item = get_string("Add item", "item")
    if item:
        items.append(item)  # add item, list is mutable
        items.sort(key=str.lower)  # it will call lower() function, this is a DSU(Decorate,Sort,Undecorate) sorting
        return True  # dirty is True
    return dirty


def delete_item(items, dirty):
    index = get_integer("Delete item number (or 0 to cancel)", "number", maximum=len(items))
    if index != 0:
        del items[index - 1]  # delete item in a list, list is mutable
        return True  # dirty is true
    return dirty


def save_list(filename, items, terminating=False):  # return dirty
    fh = None  # file handler
    try:
        fh = open(filename, "w", encoding="utf8")
        fh.write("\n".join(items))
        fh.write("\n")
    except EnvironmentError as err:
        print("ERROR: failed to sae {0}: {1}".format(filename, err))
        return True
    else:
        print("Saved {0} item{1} to {2}".format(len(items), ("s" if len(items) > 1 else ""), filename))
        if not terminating:
            input("Press Enter to continue...")
        return False
    finally:
        if fh is not None:
            fh.close()


def load_list(filename):  # return a list
    items = []
    fh = None
    try:
        for line in open(filename, encoding="utf8"):  # read all lines in file
            items.append(line.rstrip())  # right strip
    except EnvironmentError as err:
        print("RROR: failed to load {0}: {1}".format(filename, err))
        return []
    finally:
        if fh is not None:
            fh.close()
    return items


def get_string(message, name="string", default=None, minimum_lenght=0, maximum_length=80):
    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line:
                if default is not None:
                    return default
                if minimum_lenght == 0:
                    return ""
                else:
                    raise ValueError("{0} may not be empty".format(name))
            if not (minimum_lenght <= len(line) <= maximum_length):
                raise ValueError(
                    "{name} must have at least {minimum_length} and at most {maximum_length} characters".format(
                        **locals()))
            return line
        except ValueError as err:  # ValueError ? enter a Enter?
            print("ERROR", err)


def get_integer(message, name="integer", default=None, minimum=0, maximum=80, allow_zero=True):
    class RangeError(Exception):
        pass

    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            i = int(line)
            if i == 0:
                if allow_zero:
                    return i
                else:
                    raise RangeError("{0} may not be 0".format(name))
            if not (minimum <= i <= maximum):
                raise RangeError("{name} must be between {minimum_length} and {maximum_length} inclusive {0}".format(
                    "(or 0)" if allow_zero else "", **locals()))
            return i
        except RangeError as err:
            print("ERROR", err)
        except ValueError as err:
            print("ERROR {0} must be an integer".format(name))

main()