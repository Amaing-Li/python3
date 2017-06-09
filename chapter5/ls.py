#!/usr/bin/env python3

import locale

locale.setlocale(locale.LC_ALL, "")  # setlocale(category, locale=None)

import datetime
import optparse
import os


def main():
    counts = [0, 0]
    opts, paths = process_options()  ##
    if not opts.recursive:  # not recursive
        filenames = []
        dirnames = []
        for path in paths:
            if os.path.isfile(path):
                filenames.append(path)
                continue
            for name in os.listdir(path):  # get here, it is a directory
                if not opts.hidden and name.startswith("."):
                    continue
                fullname = os.path.join(path, name)
                if fullname.startswith("./"):
                    fullname = fullname[2:]  # current directory, there is no need of './'
                if os.path.isfile(fullname):
                    filenames.append(fullname)
                else:
                    dirnames.append(fullname)
        counts[0] += len(filenames)
        counts[1] += len(dirnames)
        process_lists(opts, filenames, dirnames)  ##
    else:  # recursive
        for path in paths:
            for root, dirs, files in os.walk(path):
                if not opts.hidden:
                    dirs[:] = [dir for dir in dirs if not dir.startswith(".")]  # exclude hidden directories
                filenames = []
                for name in files:
                    if not opts.hidden and name.startswith("."):
                        continue  # exclude hidden files
                    fullname = os.path.join(root, name)
                    if fullname.startswith("./"):
                        fullname = fullname[2:]
                    filenames.append(fullname)
                counts[0] += len(filenames)
                counts[1] += len(dirs)
                process_lists(opts, filenames, [])  ##
    print("{0} file{1}, {2} director{3}".format("{0:n}".format(counts[0]) if counts[0] else "no",
                                                "s" if counts[0] != 1 else "",
                                                "{0:n}".format(counts[1]) if counts[1] else "no",
                                                "ies" if counts[1] != 1 else "y"))


def process_options():
    usage = """%prog [options] [path1 [path2 [... pathN]]]
    The paths are optional; if not given . is used"""
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-H", "--hidden", dest="hidden", action="store_true", help=("show hidden files [default: off]"))
    parser.add_option("-m", "--modified", dest="modified", action="store_true",
                      help=("show last modified date/time [default: off]"))
    orderlist = ["name", "n", "modified", "m", "size", "s"]
    parser.add_option("-o", "--order", dest="order", choices=orderlist,
                      help=("order by {0} [default: %default]".format(", ".join(["'" + x + "'" for x in orderlist]))))
    parser.add_option("-r", "--recursive", dest="recursive", action="store_true",
                      help=("recurse into subdirectories [default: off]"))
    parser.add_option("-s", "--sizes", dest="sizes", action="store_true", help=("show sizes [default: off]"))
    parser.set_defaults(order=orderlist[0])
    opts, args = parser.parse_args()
    if not args:
        args = ["."]
    return opts, args


def process_lists(opts, filenames, dirnames):
    keys_lines = []
    for name in filenames:
        modified = ""
        if opts.modified:
            try:
                # 2008-02-11 14:17:03
                modified = (datetime.datetime.fromtimestamp(os.path.getmtime(name)).isoformat(" ")[:19] + " ")
            except EnvironmentError:
                modified = "{0:>19} ".format("unknown")
        size = ""
        if opts.sizes:
            try:
                size = "{0:>15n} ".format(os.path.getsize(name))
            except EnvironmentError:
                size = "{0:>15} ".format("unknown")  ## it is easier to ask forgiveness than permission
        if os.path.islink(name):
            name += " -> " + os.path.realpath(name)
        if opts.order in {"m", "modified"}:
            orderkey = modified
        elif opts.order in {"s", "size"}:
            orderkey = size
        else:
            orderkey = name
        keys_lines.append((orderkey, "{modified}{size}{name}".format(**locals())))
    size = "" if not opts.sizes else " " * 15
    modified = "" if not opts.modified else " " * 20
    for name in sorted(dirnames):
        keys_lines.append((name, modified + size + name + "/"))  # add a sign '/' for dircectory
    for key, line in sorted(keys_lines):
        print(line)


main()
