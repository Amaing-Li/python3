import datetime  # for creating datetime.data and datetime.time objects
import \
    xml.sax.saxutils  # escape function: takes a string and returns an equivalent string with the special HTML characters in their escape forms

COPYRIGHT_TEMPLATE = "Copyright (c) {0} {1}. All rights reserved."
STYLESHEET_TEMPLATE = ('link rel="stylesheet" type="text/css" media="all" href="{0}" />\n')
# just as it name says, stylesheet is a file(sheet) that controls the html style
HTML_TEMPLATE = """<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" \
"html://www.w3.org/TR/xhtml1/DTD/xhtml-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>{title}</title>
<!-- {copyright} --->
<meta name="Description" content="{description}" />
<meta name="Keywords" content="{keywords}" />
<meta equiv="content-type" content-"text/html"; charset=utf-8" />
{stylesheet}\
</head>
<body>

</body>
</html>
"""


class CancelledError(Exception): pass  # user defined exception, extends Exception


# this method stands for the hole thought structure
# if a process is complex enough or used commonly, then make it a variable or method
# it is better to think the problem forward and backward and write in whichever order you like
def main():
    information = dict(name=None, year=datetime.date.today().year, filename=None, title=None, description=None,
                       keywords=None, stylesheet=None)  # dictionary just like a map in java and scala,
    while True:
        try:
            print("\nMake HTML Skeleton\n")
            populate_information(information)  # update information
            make_html_skeleton(**information)  # use the information to make the skeleton
        except CancelledError:  # user defined exception to control work flow
            print("Cancelled")
        if (get_string("\nCreate another (y/n)?", default="y").lower() not in {"y",
                                                                               "yes"}):  # loop to generate another html file
            break


def populate_information(information):
    # def get_string(message, name="string", default=None, minimum_length=0, maximum_length=80)
    name = get_string("Enter your name (for copyright)", "name", information["name"])
    if not name:
        raise CancelledError()
    year = get_integer("Enter copyright year", "year", information["year"], 2000, datetime.date.today().year + 1, True)
    if year == 0:
        raise CancelledError()
    filename = get_string("Enter filename", "filename")
    if not filename:
        raise CancelledError()
    if not filename.endswith((".htm", ".html")):
        filename += ".html"
    title = get_string("Enter title", "title")
    if not title:
        raise CancelledError()
    description = get_string("Enter a keyword (optional)", "description")
    keywords = []
    while True:
        keyword = get_string("Enter a keyword (optional)", "keyword")
        if keywords:
            keywords.append(keyword)
        else:
            break
    stylesheet = get_string("Enter the stylesheet filename ", "(optional)", "stylesheet")
    if stylesheet and not stylesheet.endswith(".css"):
        stylesheet += ".css"

    information.update(name=name, year=year, filename=filename, title=title, description=description, keywords=keywords,
                       stylesheet=stylesheet)


def make_html_skeleton(year, name, title, description, keywords, stylesheet, filename):
    copyright = COPYRIGHT_TEMPLATE.format(year, xml.sax.saxutils.escape(name))
    title = xml.sax.saxutils.escape(title)
    description = xml.sax.saxutils.escape(description)
    keywords = ",".join([xml.sax.saxutils.escape(k) for k in
                         keywords]) if keywords else ""  # conditional expression,  embedded is a list comprehension
    stylesheet = STYLESHEET_TEMPLATE.format(stylesheet) if stylesheet else ""
    html = HTML_TEMPLATE.format(**locals())  # mapping uppacking

    fh = None  # file handler
    try:
        fh = open(filename, "w", encoding="utf-8")  # w: write
        fh.write(html)
    except EnvironmentError as err:
        print("ERROR", err)
    else:
        print("Saved skeleton", filename)  # if the try_suite finished normally, this else_suite is executed
    finally:
        if fh is not None:
            fh.close()


def get_string(message, name="string", default=None, minimum_length=0, maximum_length=80):
    message += ": " if default is None else " [{0}]: ".format(default)  # if...else... expression
    while True:
        try:
            line = input(message)  # get input from console
            if not line:  # not true, that is false, empty
                if default is not None:
                    return default
                if minimum_length == 0:  # go here, name is None and default is None
                    return ""
                else:
                    raise ValueError("{0} may not be empty".format(name))
            if not (minimum_length <= len(
                    line) <= maximum_length):  # restrict line's length, python support this format comparison
                raise ValueError(
                    "{name} must have at least {minimum_length} and at most {maximum_length} characters".format(
                        **locals()))
            return line
        except ValueError as err:
            print("ERROR", err)


def get_integer(message, name="integer", default=None, minimum=0, maximum=1, allow_zero=True):
    class RangeError(Exception):
        pass

    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            i = int(line)
            if i == 0:
                if allow_zero:
                    return i
                else:
                    raise RangeError("{0} may not to be 0".format(name))
            if not (minimum <= i <= maximum):
                raise RangeError(
                    "{name} must be between {minimun} and {maximum} inclusive{0}".format(" (or 0" if allow_zero else "",
                                                                                         **locals()))
            return i
        except RangeError as err:
            print("ERROR", err)
        except ValueError as err:
            print("ERROR {0} must be an integer".format(name))


main()
