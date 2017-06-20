import SortedList


class SortedDict(dict):
    # make use of the dict method
    def __init__(self, dictionary=None, key=None, **kwargs):
        dictionary = dictionary or {}
        super().__init__(dictionary)  # dict.__init__()
        if kwargs:
            super().update(kwargs)
        self.__keys = SortedList.SortedList(super().keys(), key)
        # keep a copy of all the dictionary's keys in a sorted list stored in the self.__keys vairable
        # we must not use SortedDict.keys() because that relies on the self.__keys variable
        # which will exist only afte the SortedList of keys has been created

    def update(self, dictionary=None, **kwargs):  # make heavy use of dict.update()
        """update one dictionary's items with another dictionary's items or with keyword arguments, or both"""
        if dictionary is None:
            pass
        elif isinstance(dictionary, dict):
            super().update(dictionary)
        else:
            for key, value in dictionary.items():
                super().__setitem__(key, value)
        if kwargs:
            super().update(kwargs)
        # to avoid self.__keys list becomes out of date
        self.__keys = SortedList.SortedList(super().keys(), self.__keys.key)

    # the dict API includes the dict.fromkeys() class method
    # this method is used to create a new dictionary based on an iterable.
    # When inherited class methods are called, their cls vairable is set to the correct class,
    # just like when normal methods are called and their self variable is set to the current object.
    # This is dirrerent from and better than using a static method because a static method is tied to
    # a particular class and does not know whether it is being executed in the context of its original class
    # or that of a subclass
    @classmethod
    def fromkeys(cls, iterable, value=None, key=None):
        return cls({k: value for k in iterable}, key)

    # to implement the d[key]=value syntax
    def __setitem__(self, key, value):
        if key not in self:
            self.__keys.add(key)
        return super().__setitem__(key, value)  # super() is essential to avoid infinite recursion

    # we do not reimplement the __getitem__() method
    # since the base class version works fine and has no effect on the ordering of the keys

    # del d[key] syntax
    def __delitem__(self, key):
        try:
            self.__keys.remove(key)
        except ValueError:
            raise KeyError(key)
        return super().__delitem__(key)

    def setdefault(self, key, value=None):
        """returns the value for the given key
        if the key is not in the dictionary;
        otherwise, it creates a new item with the given key
        and the value and returns the value"""
        if key not in self:
            self.__keys.add(key)
        return super().setdefault(key, value)

    # the pop() method must support two different behaviors to match dict.pop()
    # The first is d.pop(k); here the value for key k is returned,
    # or if there is no key k, a KeyError is raised.
    # The second is d.pop(k,value); here the value for key k is returned,
    # or if there is no key k, vlaue is returned.
    def pop(self, key, *args):
        if key not in self:
            if len(args) == 0:
                raise KeyError(key)
            return args[0]
        self.__keys.remove(key)
        return super().pop(key, args)

    def popitem(self):
        """removes and returns a random key-value item from the dictionary"""
        item = super().popitem()
        self.__keys.remove(item[0])
        return item

    def clear(self):
        super().clear()
        self.__keys.clear()

    # generator method
    def values(self):
        for key in self.__keys:
            yield self[key]

            # generator method

    def items(self):
        for key in self.__keys:
            yield (key, self[key])

    # for iter(d) syntax
    def __iter__(self):
        return iter(self.__keys)

    # since the __iter__() method and the keys() method have identical behavior,
    # instead of implementing keys(), we simply create an object reference called keys and
    # set it to refer to the __iter__() method
    keys = __iter__

    # We cannot provide an eval()-able representation of a SortedDict because we can't produce
    # an eval()-able representation of the key function.
    def __repr__(self):
        return object.__repr__(self)

    def __str__(self):
        return "{" + ", ".join(["{0!r}: {1!r}".format(k, v) for k, v in self.items()] + "}")

    # The base class methods dict.get(), dict.__getitem__(), dict.__len__(), and
    # dict.__contains__() all work fine as they are and don't affect the key ordering,
    # so we have not needed to reimplement them

    # The easiest reimplementation is simply def copy(self): return SortedDict(self)
    # We've chosen a slightly more complicated solution that avoids re-sorting
    # the already sorted keys.
    def copy(self):
        d = SortedDict()  # create an empty sorted dictionary
        super(SortedDict, d).update(self)  # equals to dict.update(d,self)
        # update it with the items in the original sorted dictionary
        # using the base class dict.update() to avoid the SortedDict.update() reimplementation
        d.__keys = self.__keys.copy()  # shallow copy
        return d
        # When super() is called with no arguments it works on the base class
        # and the self object. But we can make it work on any class and any object
        # by passing in a class and an object explicitly.

    __copy__ = copy  # copy.copy() uses our custom copy method


    def value_at(self,index):
        # thanks to inheritance, we can look up values in the SortedDict
        # using the item access oprator([]) applied directly to self,
        # since self is a dict. If an out-of-range index is given
        # the methods raise an indexError exception
        return self[self.__keys[index]]


    def set_value_at(self,index,value):
        self[self.__keys[index]] = value


class MyDict(SortedDict): pass


d = MyDict.fromkeys("VEINS", 3)
print(str(d))  # {'V': 3, 'E': 3, 'I': 3, 'N': 3, 'S': 3}
print(d.__class__.__name__)  # MyDict
# When inherited class methods are called, their cls vairable is set to the correct class,
# just like when normal methods are called and their self variable is set to the current object.
# This is dirrerent from and better than using a static method because a static method is tied to
# a particular class and does not know whether it is being executed in the context of its original class
# or that of a subclass
