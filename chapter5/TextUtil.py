#!/usr/bin/env python3

# docstrings
"""
This module provides a few string manipulation functions.

>>> is_balanced("(Python (is (not (lisp))))")
True
>>> shorten("The Crossing",10)
'The Cro...'
>>> simplify(" some   text   with  spurious whitespace  ")
'some text with spurious whitespace'
"""

import string


def simplify(text, whitespace=string.whitespace, delete=""):
    # docstrings
    # a single line description, a blank line, further description, and then some examples
    # raw triple quoted string, because the quoted strings are inside a docstring

    r"""Returns the text with multiple spaces reduced to single spaces
    
    The whitespace parameter is a string of characters, each of which is considered to be a space.
    If delete is not empty it should be a string, in which case any characters in the delete string 
    are execluded from the resultant string.
    
    >>> simplify(" this    and \n that\t too")
    'this and that too'
    >>> simplify("  Washington  D.C\n")
    'Washington  D.C.'
    >>> simplify(" Washington  D.C.\n, delete=",;:.)
    'Washington DC'
    >>> simplify(" disemvoweled ", delete="aeiou")
    'dsmvwld'
    """

    result = []
    word = ""
    for char in text:
        if char in delete:
            continue
        elif char in whitespace:  # encounter a whitespace
            if word:  # "" equals False
                result.append(word)  # terminate character accumulation and append the current word
                word = ""  # character accumulation from ""
        else:
            word += char  # character by character to form a word
    if word:
        result.append(word)  # append the last word
    return " ".join(result)


def is_balanced(text, brackets="()[]{}<>"):
    counts = {}  # {} stands for set or dictionary, but empty set must create using set(), so this is a dict
    left_for_right = {}  # dict
    for left, right in zip(brackets[::2], brackets[1::2]):
        assert left != right, "the bracket characters must differ"  # if left == right, the message is given
        counts[left] = 0
        left_for_right[right] = left
    for c in text:
        if c in counts:
            counts[c] += 1
        elif c in left_for_right:
            left = left_for_right[c]
            if counts[left] == 0:  # if the count for that character is 0 it means
                # we have reached one closing character to0 many times so can immediately return False
                return False
            counts[left] -= 1
    return not any(counts.values())  # any function: if any is True(not 0) the result is True


def shorten(text, length=25, indicator="..."):
    """Returns text or a truncated copy with the indicator added
    
    text is any string; length is the maximum length of the returned
    string (excluding any indicator); indicator is the string added at 
    the end to indicate that the text has been shortened
    
    >>> shorten("Second Variety")
    'Second Variety'
    >>> shorten("Voices from the Street",14)
    'Voices from th...'
    >>> shorten("Radio Free Albemuth",9,"*")
    'Radio Fre*'
    """

    if len(text) > length:
        text = text[:length] + indicator
    return text


if __name__ == "__main__":
    import doctest
    doctest.testmod()