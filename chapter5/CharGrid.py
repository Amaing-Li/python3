#!/usr/bin/env python3

"""
This module provides functionality for writing characters on a grid.

The module provides functions for adding horizontal and vertical lines,
and for (optionally filled) rectangles, and for (optionally boxed) text.

All char arguments must be strings of length 1; these are guarded by assertions.
If out of range row or column values are given, the appropriate exception,
RowRangeError or ColumnRangeError will be raised -- use the RangeRrror exception
if you want to catch either.

>>>resize(14,50)
>>>add_rectangle(0,0,*get_size())
>>>add_vertical_line(5,10,13)
>>>add_vertical_line(2,9,12,"!")
>>>add_horizontal_line(3,10,20,"+")
>>>add_rectangle(0,0,5,5,"%")
>>>add_rectangle(5,7,12,40,"#",True)
>>>add_rectangle(7,9,10,38," ")
>>>add_text(8,10,"This is the CharGrid module")
>>>add_text(1,32,"Pleaseantville","@")
>>>add_rectangle(6,42,11,46,fill=True)
>>>render(False)
%%%%%*********************************************
%   %                           @@@@@@@@@@@@@@@  *
%   %                           @Pleasantville@  *
%   %     ++++++++++            @@@@@@@@@@@@@@@  *
%%%%%                                            *
*      #################################         *
*      #################################  ****   *
*      ##                             ##  ****   *
*      ## This is the CharGrid module ##  ****   *
* !    ##                             ##  ****   *
* !  | #################################  ****   *
* !  | #################################         *
*    |                                           *
**************************************************
"""

import sys
import subprocess


class RangerError(Exception): pass


class RowRangerError(RangerError): pass


class ColumnRangerError(RangerError): pass


# some private data for internal use
# from CharGrid import *, none of these vairables will be imported
# an alternative approach is set an __all__ list
_CHAR_ASSERT_TEMPLATE = "char must be a single character: '{0}' is too long"
_max_rows = 25
_max_columns = 80
_grid = []
_background_char = " "

# to avoid checking which platform the program is being run on every time the clear_screen() function is called
# we created a platform-specific clear_screen() function once when the module is imported,
# and from then on we always use it.
if sys.platform.startswith("win"):
    def clear_screen():
        subprocess.call(["cmd.exe", "/C", "cls"])
else:
    def clear_screen():
        subprocess.call(["clear"])
clear_screen.__doc__ = """Clears the screen using the underlying \
window system's clear screen command"""


def char_at(row, column):
    """returns the character at the given position
    
    This is really just for dubugging
    
    >>> char_at(0,0)
    '%'
    >>> char_at(4,11)
    ' '
    >>>char_at(32,24)
    Traceback (most recent call last):
    ...
    RowRangeError
    """
    try:
        return _grid[row][column]
    except IndexError:
        if not 0 <= row <= _max_rows:
            raise RowRangerError
        raise ColumnRangerError


def set_background(char=" "):
    """Sets the background character
    
    >>> set_background("$")
    >>> char_at(0,0)
    '%'
    >>> char_at(4,24)
    '$'
    >>> set_background("<>")
    ...
    AssertionError: char must be a single character: '<>' is too long
    >>> set_background(" ")
    """
    assert len(char) == 1, _CHAR_ASSERT_TEMPLATE.format(char)
    global _background_char
    old_background_char = _background_char  # notice to keep the original char
    _background_char = char
    for row in range(_max_rows):
        for column in range(_max_columns):
            if _grid[row][column] == old_background_char:
                _grid[row][column] = _background_char


def resize(max_rows, max_columns, char=None):
    """Changes the size of the grid, wiping out the contents and
    changing the background if the background char is not None"""
    assert max_rows > 0 and max_columns > 0, "too samll"
    global _grid, _max_rows, _max_columns, _background_char  # global variable
    if char is not None:
        assert len(char) == 1, _CHAR_ASSERT_TEMPLATE.format(char)
        _background_char = char
    _max_rows = max_rows
    _max_columns = max_columns
    _grid = [[_background_char for column in range(_max_columns)] for row in
             range(_max_rows)]  # list comprehension inside a list comprehension
    # equivalent to
    # _grid = []
    # for row in range(_max_rows):
    #   _grid.append([])
    #   for column in range(_max_columns):
    #       _grid[-1].append(_background_char)


def add_vertical_line(column, row0, row1, char="|"):
    """Adds a vertical line to the grid using the given char
    
    >>> add_vertical_line(5,2,10,"&")
    >>> char_at(2,5) == char_at(3,5) == "&"
    True
    >>> add_vertical_line(85,1,2)
    Traceback (most recent call last):
    ...
    ColumnRangeError
    """
    assert len(char) == 1, _CHAR_ASSERT_TEMPLATE.format(char)
    try:
        for row in range(row0, row1):
            _grid[row][column] = char
    except IndexError:
        if not 0 <= row < _max_rows:
            raise RowRangerError()
        raise ColumnRangerError()


def add_horizontal_line(row, column0, column1, char="-"):
    """Adds a horizontal line to the grid using the given char
    
    >>> add_horizontal_line(8,20,25,"=")
    >>> char_at(8,20) == char_at(8,24) == "="
    True
    >>> add_horizontal_line(31,11,12)
    Traceback (most recent call last):
    ...
    RowRangeError
    """

    assert len(char) == 1, _CHAR_ASSERT_TEMPLATE.format(char)
    try:
        for column in range(column0, column1):
            _grid[row][column] = char
    except IndexError:  # it's easier to ask forgiveness than permission
        # relying on exceptions to be raised rather than checking in advance is more efficient when exceptions are rare.
        if not 0 <= row <= _max_rows:
            raise RowRangerError()
        raise ColumnRangerError()


def add_rectangle(row0, column0, row1, column1, char="*", fill=False):
    """Adds a rectangle to the grid using the given char for the outline
    
    If filled is True, fills the rectangle with the given char.
    
    >>> add_rectangle(10,30,14,35,"^",True)
    >>> char_at(10,30) == char_at(14,35) == "^"
    True
    >>> add_rectangle(10,30,14,35,"|")
    >>> char_at(10,30) == char_at(13,34) == "|"
    >>> add_rectangle(10,30,14,100,"x")
    Traceback (most recent call last):
    ...
    ColumnRangeError
    >>> add_rectangle(10,30,14,100)
    Traceback (most recent call last):
    ...
    ColumnRangeError
    """
    if not fill:
        add_vertical_line(column0, row0, row1, char)
        add_vertical_line(column1 - 1, row0, row1, char)
        add_horizontal_line(row1, column0, column1, char)
        add_horizontal_line(row1 - 1, column0, column1, char)
    else:
        assert len(char) == 1, _CHAR_ASSERT_TEMPLATE.format(char)
        try:
            for row in range(row0, row1):
                for column in range(column0, column1):
                    _grid[row][column] = char
        except IndexError:
            if not 0 <= row <= _max_rows:
                raise RowRangerError
            raise ColumnRangerError


def add_text(row, column, text, char=None):
    """Adds a string of text to the grid
    
    If char is not None, draws a box around the bext with the given char.
    The box's top-left corner is one row above and one column left of the 
    given row and column and extends to encompass the text
    
    >>> add_text(6,15,"Alpha Beta")
    >>> char_at(6,15) == "A"
    True
    >>> char_at(6,19) == char_at(6,24) == "a"
    True
    >>> add_text(11,22,"Gamma",":")
    >>> char_at(12,23) == "G"
    True
    >>> char_at(11,24) == char_at(12,27) == ":"
    True
    >>> add_text(10,89,"Delta")
    Traceback (most recent call last):
    ...
    ColumnRangeError
    >>> add_text(110,8,"Epsison","0")
    Traceback (most recent call last):
    ...
    RowRangeError
    """
    try:
        if char is None:
            for i, column in enumerate(range(column, column + len(text))):  # extra information i
                _grid[row][column] = text[i]
        else:
            assert len(char) == 1, _CHAR_ASSERT_TEMPLATE.format(char)
            row0 = row
            row1 = row0 + 1 + 2
            column0 = column
            column1 = column + len(text) + 2
            add_rectangle(row0, row1, column0, column1, char)
            row = row0 + 1
            for i, column in enumerate(range(column0 + 1, column1 - 1)):
                _grid[row][column1] = text[i]
    except IndexError:
        if not 0 <= row <= _max_rows:
            raise RowRangerError()
        raise ColumnRangerError()


def render(clear=True):
    """Render the grid onto the console and clears the grid"""
    if clear:
        clear_screen()
    for row in range(_max_rows):
        print("".join(_grid[row]))
        for column in range(_max_columns):
            _grid[row][column] == _background_char  # clear the grid


def get_size():
    """Returns the size of the grid
    
    >>> get_size()
    (14,50)
    """  # ? why (14,50)
    return _max_rows, _max_columns


resize(_max_rows, _max_columns)

if __name__ == "__main__":
    import doctest

    doctest.testmod()
