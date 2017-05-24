import sys

if len(sys.argv) < 3:
    print("usage: grepword.py word infile1 [infile2 [... infileN]]")
    sys.exit()

word = sys.argv[1]
for filename in sys.argv[2:]:
    # The enumerate() function takes an iterator and returns an enumerator object.
    # This object can be treated like a iterator,
    #  and at each iteration it returns a 2-tuple
    # with the tuple's first item the iteration number(by default starting from 0)
    # and the second item the next item from the iterator enumerator() was called on
    for lino, line in enumerate(open(filename), start=1):
        if word in line:
            print("{0}:{1}:{2:.40}".format(filename, lino, line.rstrip()))
