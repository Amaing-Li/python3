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
        index = get_integer("Specify file's number (or 0 to create ", "a new one", "number", maximum=len(files),
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
        width = 1 if len(items) <10 else 2 if len(items) <100 else 3  # embedded conditional comprehension, digit format requirement
        for i,item in enumerate(items):  # enumerate, add a indexer
            print("{0:{width}}: {item}".format(i+1,**locals()))  # start from 1, format with mapping unpacking
    print()  # a new blank line


def get_choice(items,dirty):
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

        choice = get_string(menu,"choice","a")  ## function

        if choice not in valid_choices:
            print("ERROR: invalid choice -- enter one of '{0}'".format(valid_choices))
            print("Press Enter to continue...")
        else:
            return choice


def add_item(items,dirty):
    pass

def delete_item(items,dirty):
    pass

def save_list(filename,items,terminating=False):
    pass

def load_list(filename):
    pass

def get_string(message,name="string",default=None,minimum_lenght=0,maximum_length=80):
    pass


def get_integer(message,name="integer",default=None,minimum_length=0,maximum_length=80,allow_zero=True):
    pass


