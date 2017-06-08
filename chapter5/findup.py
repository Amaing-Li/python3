import os
import sys
import collections

path = sys.argv[1] if len(sys.argv) > 1 else "."
data = collections.defaultdict(list)

# dictionary, key is fullname, value is mtime
date_from_name = {}
for name in os.listdir(path):
    fullname = os.path.join(path,name)
    if os.path.isfile(fullname):
        date_from_name[fullname] = os.path.getmtime(fullname)

# defaultdict, key is (filename_size, filename), value is fullname
for root, dirs, files in os.walk(path):  # os.walk() returns the root and two lists,
    # one of the subdirectories and the other the files
    for filename in files:
        fullname = os.path.join(root, filename)
        key = (os.path.getsize(filename), filename)
        data[key].append(fullname)

for size, filename in sorted(data):
    names = data[(size, filename)]
    if len(names) > 1:
        # like:
        # \windows\system32\shell32.dll
        # \windows\system32\dllcache\shell32.dll
        print("{filename} ({size} bytes) may be duplicated ({0} files):".format(len(names), **locals()))
        for name in names:
            print("\t{0}".format(name))
