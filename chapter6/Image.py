"""this module provides the Image class which holds (x,y,color) triples
and a background color to provide a kind of sparse-array representation of 
an image. A method to export the image in XPM format is also provided"""

import os
import pickle


class ImageError(Exception): pass


class CoordinateError(ImageError): pass


class LoadError(ImageError): pass


class SaveError(ImageError): pass


class ExportError(ImageError): pass


class NoFilenameError(ImageError): pass


# 2 way to store a image
# for example: 100x100 image
# 1. store 10000 colors
# 2. store a single background color plus the colors of those points that differ from the background color
class Image:
    def __init__(self, width, height, filename="", background="#FFFFFF"):
        self.filename = filename
        self.__background = background
        self.__data = {}  # keys are (x,y) coordinates and values are color strings
        self.__width = width
        self.__height = height
        self.__colors = {self.__background}

    @property
    def background(self):
        return self.__background

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def colors(self):
        return set(self.__colors)

    # to support []
    def __getitem__(self, coordinate):
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] <= self.width) or not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        return self.__data.get(tuple(coordinate), self.__background)  # keys are tuple standing for coordinate

    def __setitem__(self, coordinate, color):
        """Sets the color at the given (x,y) coordinate"""
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] <= self.width) or not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        if color == self.__background:
            self.__data.pop(tuple(coordinate), None)
        else:
            self.__data[tuple(coordinate)] = color
            self.__colors.add(color)

    def __delitem__(self, coordinate):
        """Delete the color at the given (x,y) coordinate
        
        In effect this makes the coordinate's color the background color."""

        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] <= self.width) or not (0 <= coordinate[1] <= self.height)):
            raise CoordinateError(str(coordinate))
        self.__data.pop(tuple(coordinate), None)

        # both __setitem__() and __delitem__() have the potential to make the set of colors
        # contain more colors than the images actually uses.
        # we have chosen to accept the trade-off of potentially having more colors
        # in the color set than are actually used for the sake of better performance,
        # that is, to make setting and deleting a color as fast as possible -- especially
        # since storing a few more colors isn't usually a problem.

    def save(self, filename=None):
        """Save the current image, or the one specified by filename
        
        If filename is specified the internal filename is set to it"""
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            data = [self.width, self.height, self.__background, self.__data]
            fh = open(self.filename, "wb")
            # The pickle module can serialize data using various formats
            # with the one to use specified by the third argument to
            # pickle.dump(). Protocol 0 is ASCII and ti usefull for debugging.
            # we have used protocol 3 (pickle.HIGHEST_PROTOCOL), a compact binary format
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PicklingError) as err:
            raise SaveError(str(err))
        finally:
            if fh is not None:
                fh.close()

    def load(self, filename=None):
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()
        fh = None
        try:
            fh = open(self.filename, "rb")
            data = pickle.load(fh)
            self.__width, self.__height, self.__background, self.__data = data
            self.__colors = (set(self.__data.values()) | {self.__background})
        except (EnvironmentError, pickle.UnpicklingError) as err:
            raise LoadError(str(err))
        finally:
            if fh is not None:
                fh.close()

    def export(self, filename):
        if filename.lower().endswith(".xpm"):
            self.__export_xpm(filename)
        else:
            raise ExportError("unsupported export format: " + os.path.splitext(filename)[1])  # extension

    def __export_xpm(self, filename):
        """Exports the image as an XPM file if less than 8930 colors are used"""
        name = os.path.splitext(os.path.basename(filename))[0]
        # >>> os.path.splitext(os.path.basename("/a/b/a.txt"))[0]
        # 'a'
        # >>> os.path.splitext(os.path.basename("/a/b/a.txt"))[1]
        # '.txt'
        count = len(self.__colors)  # the color mount
        # Using chars to stand for color
        chars = [chr(x) for x in range(32, 127) if chr(x) != '"']  # unicode point # exclude "
        if count > len(chars):
            chars = []
            for x in range(32, 127):
                if chr(x) == '"':  # exclude "
                    continue
                for y in range(32, 127):
                    if chr(y) == '"':
                        continue
                    chars.append(chr(x) + chr(y))  # 126 x 126 = 15876
        chars.reverse()
        if count > len(chars):
            raise ExportError("cannot export XPM: too many colors")
        fh = None
        try:
            fh = open(filename, "w", encoding="ascii")
            fh.write("/* XPM */\n")
            fh.write("static char *{0}[] = {{\n".format(name))
            fh.write("/* columns rows colors chars-per-pixel */\n")
            fh.write('"{0.width} {0.height} {1} {2}",\n'.format(self, count, len(chars[0])))
            char_for_color = {}
            for color in self.__colors:
                char = chars.pop()
                fh.write('"{char} c {color}",\n'.format(**locals()))
                char_for_color[color] = char  # key is color and value is char
            fh.write("/* pixels */\n")
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    color = self.__data.get((x, y), self.__background)  # get the positional pixel color or background
                    row.append(char_for_color[color])  # store the corresponding char
                fh.write('"{0}",\n'.format("".join(row)))
            fh.write("};\n")
        except EnvironmentError as err:
            raise ExportError(str(err))
        finally:
            if fh is not None:
                fh.close()

    if __name__ == "__main__":
        import doctest
        doctest.testmod()
