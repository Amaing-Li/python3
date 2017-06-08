import gzip
import io
import sys
import xml

if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
    print("usage: {0} filename".format(sys.argv[1]))

filename = sys.argv[1]
binary = gzip.open(filename).read()  # for .gz file
fh = io.StringIO(binary.decode("utf8"))  # to convert the binary data to a string

tree = xml.etree.ElementTree.ElementTree()
root = tree.parse(fh)
stations = []
for element in tree.getiterator(
        "station_name"):  # returns an iterator
    # that returns all the xml.etree.ElementTree.Element objects
    # that have the given tag name
    stations.append(element.text)  # to retrieve the text
