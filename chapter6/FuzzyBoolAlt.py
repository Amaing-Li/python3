class FuzzyBool(float):
    def conjunction(*fuzzies):
        return FuzzyBool(min(fuzzies))

    def __new__(cls, value=0.0):
        # when we create a new class it is usually mutable and relies on object.__new__()
        # to create the raw uninitialized object.
        # but in the case of immutable classes we need to do the creation and initialization
        # in one step since once an immutable object has been created it cannot be changed
        # the __new__() method is called before any object has been created,
        # so it cannot have a self object passed to it since one doesn't exist
        # in fact, __new__() is a class method
        # class methods are set up by using the built-in classmethod() function used as a decorator
        # but as a convenience we don't have to bother writing @classmethod before def __new__()
        # because Python already knows that this method is always a class method
        return super().__new__(cls, value if 0.0 <= value <= 1.0 else 0.0)

    def __invert__(self):
        return FuzzyBool(1.0 - float(self))  # polymophisim

    def __and__(self, other):
        return FuzzyBool(min(self, other))

    def __iand__(self, other):
        return FuzzyBool(min(self, other))

    def __or__(self, other):
        return FuzzyBool(max(self, other))

    def __ior__(self, other):
        return FuzzyBool(max(self, other))

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, super().__repr__())

    def __bool__(self):
        return self > 0.5

    def __int__(self):
        return round(self)

        # unimplement
        # def __add__(self, other):
        #   raise NotImplementedError()

    # mimic the behavior of Python's built-in classes
    def __and__(self, other):
        raise TypeError("unsupported operand types(s) for +: '{0}' and '{1}'".format(self.__class__.__name__,
                                                                                     other.__class__.__name__))

    def __eq__(self, other):
        # if a method implementing a comparison operator(<,<=,==,!=,>=,>) returns
        # the built-in NotImplemented object and an attempt is made to use the method,
        # Python will first try the reverse comparison by swapping the operands,
        # and if that doesn't work Python arises a TypeError exception.
        # but for all noncomparison methods that we don't want, we must raise either a
        # NotImplementedError or a TypeError exception.
        return NotImplemented

    for name, operator in (("__neg__", "-"), ("__index__", "index()")):
        message = "bad operator type for unary {0}: '{{self}}'".format(operator)
        # the built-in exec() function dynamically executes th code passed to it from the object it is given
        # by default, the code is executed in the context of the enclosing scope,
        # in this case within the definition of the FuzzyBool class
        exec("def {0}(self): raise TypeError(\"{1}\".format(self=self.__class__.__name__))".format(name, message))
