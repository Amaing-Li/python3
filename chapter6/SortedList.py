class SortedList:
    def __init__(self, sequence=None, key=None):
        _identity = lambda x: x
        self.__key = key or _identity  # wonderfull
        assert hasattr(self.__key, "__call__")  # the function is callable
        if sequence is None:
            self.__list = []
        elif (isinstance(sequence, SortedList) and sequence.key == self.__key):
            self.__list = self.__list[:]
        else:
            self.__list = sorted(list(sequence), key=self.__key)

    @property
    def key(self):
        return self.__key

    def add(self, value):
        index = self.__bisect_left(value)
        if index == len(self.__list):
            self.__list.append(value)
        else:
            self.__list.insert(index, value)

    def __bisect_left(self, value):
        key = self.__key(value)
        left, right = 0, len(self.__list)
        while left < right:
            middle = (left + right) // 2  # faster than one by one
            if self.__key(self.__list[middle]) < key:
                left = middle + 1
            else:
                right = middle
        return left

    def remove(self, value):
        index = self.__bisect_left(value)
        if index < len(self.__list) and self.__list[index] == value:
            del self.__list[index]
        else:
            # there is no the value in the list
            raise ValueError("{0}.remove(x): x not in list".format(self.__class__.__name__))

    def remove_every(self, value):
        count = 0
        index = self.__bisect_left(value)
        while (index < len(self.__list) and self.__list[index] == value):
            del self.__list[index]
            count += 1
        return count

    def count(self, value):
        count = 0
        index = self.__bisect_left(value)
        while (index < len(self.__list) and self.__list[index] == value):
            count += 1
            index += 1  ##
        return count

    def index(self, value):
        index = self.__bisect_left(value)
        if index < len(self.__list) and self.__list[index] == value:
            return index
        else:
            raise ValueError("{0}.index(x): x not in list".format(self.__class__.__name__))

    def __delitem__(self, index):
        del self.__list[index]  # we don't test for an out-of-range index since if one is given
        # the self.__list[index] call will raise an IndexError exception, which is the behavior we want

    def __getitem__(self, index):
        return self.__list[index]

    def __setitem__(self, index, value):
        raise TypeError("use add() to insert a value and rely on the list to put it in the right place")

    # if a sequence is required it is this method that is used.
    # So to convert a SortedList, L, to a plain list we can call list(L), and behind the scenes
    # PYthon will call SortedList.__iter__(L) to provide the sequence that the list() function requires.
    def iter(self):
        return iter(self.__list)

    def __reversed__(self):
        return reversed(self.__list)

    def __contains__(self, value):  # in operator
        index = self.__bisect_left(value)
        return (index < len(self.__list) and self.__list[index] == value)
        # if index < len(self.__list) and self.__list[index]==value:
        #    return True
        # else:
        #    return False

    def clear(self):
        self.__list = []

    def pop(self, index=-1):
        return self.__list.pop(index)

    def __len__(self):
        return len(self.__list)

    def __str__(self):
        return str(self.__list)

    def insert(self, index, value):
        raise AttributeError("use add() to insert a value and rely on the list to put it in the right place")

    def reverse(self):
        raise AttributeError()

    def sort(self):
        raise AttributeError()

    def copy(self):
        return SortedList(self, self.__key)

    __copy__ = copy
    # When copy.copy() is called it tries to use the object's __copy__() special method,
    # falling back to its own code if one isn't provided.
    # with this line, copy.copy() will now use the SortedList.copy() method for sorted lists
