class FuzzyBool:
    def __init__(self, value=0.0):
        self.__value = value if 0.0 <= value <= 1.0 else 0.0
        # made the value attribute private to make FuzzyBool to behave like immutable

    def __invert__(self):
        return FuzzyBool(1.0 - self.__value)

    def __and__(self, other):
        return FuzzyBool(min(self.__value, other.__value))

    def __iand__(self, other):  # in-place and
        self.__value = min(self.__value, other.__value)
        return self

    def __or__(self, other):
        return FuzzyBool(max(self.__value, other.__value))

    def __ior__(self, other):
        self.__value = max(self.__value, other.__value)
        return self

    def __repr__(self):  # eval()-able representation form
        return "{0}({1})".format(self.__class__.__name__, self.__value)
        # __class__ : a reference to the object's class

    def __str__(self):  # string form
        return str(self.__value)

    def __bool__(self):  # convert the instance to a Boolean
        return self.__value > 0.5

    def __int__(self):  # convert the instance to a int
        return round(self.__value)

    def __float__(self):  # convert the instance to a float
        return self.__value

    # to provide complete set of comparisons(<,<=,==,!=,>=,>)
    # it is necessary to implement at least three of them, <,<= and ==
    # Python will infer
    def __lt__(self, other):
        return self.__value < other.__value

    def __eq__(self, other):
        return self.__value == other.__value

    def __le__(self, other):
        return self.__value <= other.__value

    def __hash__(self):  # reimplement __eq__() so this is needed
        # hash() function: which can operate on any type which has a __hash__() special method
        # id() function returns a unique integer for the object it is given as its argument
        # usually the object's address in memory
        return hash(id(self))  # object's unique ID

    def __format__(self, format_spec):  # format specification
        # made use of the float.__format__() method
        return format(self.__value, format_spec)

    @staticmethod  # decorator
    # static methods are simply methods that do not get self or any other first argument specially passed by Python
    def conjunction(*fuzzies):  # starred parameter
        return FuzzyBool(min([float(x) for x in fuzzies]))

    # some python programmers consider the use of static methods to be un-Pythonic,
    # and use them only if they are converting code from another language (such as C++ and Java)
    # or if they have a method that does not use self
    @staticmethod
    def disconjunction(*fuzzies):
        return FuzzyBool(max(float(x) for x in fuzzies))


