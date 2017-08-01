import datetime
import gzip
import pickle
import os

import sys

import struct

import textwrap

# magic number: a sequence of one or more bytes at the beginning of a file
# that is used to indicate the file's type
GZIP_MAGIC = b"\x1F\x88"

MAGIC = b"AIB\x00"  # for custom raw binary file
FORMAT_VERSION = b"\x00\x01"  # for custom raw binary file
# I: 32-bit unsigned integer
# d: 64-bit float
# i: 32-bit signed integer
# ?: boolean
NumbersStruct = struct.Struct("<Idi?")


class IncidentError(Exception): pass


class Incident:
    def __init__(self, report_id, date, airport, aircraft_id, aircraft_type, pilot_percent_hours_on_type,
                 pilot_total_hours, midair, narrative=""):
        assert len(report_id) >= 8 and len(report_id.split()) == 1, "invalid report ID"  # no white space

        self.__report_id = report_id  # private read_only
        self.date = date
        self.airport = airport
        self.aircraft_id = aircraft_id
        self.aircraft_type = aircraft_type
        self.pilot_percent_hours_on_type = pilot_percent_hours_on_type
        self.pilot_total_hours = pilot_total_hours
        self.midair = midair
        self.narrative = narrative

    @property
    def report_id(self):
        return self.__report_id

    @property.getter  # getter could be omitted
    def date(self):
        return self.__date

    @property.setter  # property for value invalidation
    def date(self, date):
        assert isinstance(date, datetime.date), "invalid date"
        self.__date = date

    @property
    def airport(self):
        return self.__airport

    @property.setter
    def airport(self, airport):
        assert airport and "\n" not in airport, "invalid airport"  # airport nonempty and no newlines
        self.__airport = airport

    @property
    def aircraft_id(self):
        return self.__aircraft_id

    @property.setter
    def aircraft_id(self, aircraft_id):
        assert aircraft_id and "\n" not in aircraft_id, "invalid aircraft_id"  # aircraft_id nonempty and no newlines
        self.__aircraft_id = aircraft_id

    @property
    def aircraft_type(self):
        return self.__aircraft_type

    @property.setter
    def aircraft_type(self, aircraft_type):
        assert aircraft_type and "\n" not in aircraft_type, "invalid aircraft_type"
        self.__aircraft_type = aircraft_type

    @property
    def pilot_percent_hours_on_type(self):
        return self.__pilot_percent_hours_on_type

    @property.setter
    def pilot_percent_hours_on_type(self, pilot_percent_hours_on_type):
        assert 0 <= pilot_percent_hours_on_type <= 100.0, "out of range percentage"  # between 0.0 and 100.0
        self.__pilot_percent_hours_on_type = pilot_percent_hours_on_type

    @property
    def pilot_total_hours(self):
        return self.__pilot_total_hours

    @property.setter
    def pilot_total_hours(self, pilot_total_hours):
        assert pilot_total_hours > 0, "invalid number of hours"
        self.__pilot_total_hours = pilot_total_hours

    @property
    def midair(self):
        return self.__midair

    @property.setter
    def midair(self, midair):
        assert isinstance(midair, bool), "invalid midair value"
        self.__midair = midair

    @property
    def narrative(self):
        return self.__narrative

    @property.setter
    def narrative(self, narrative):
        self.__narrative = narrative

    @property
    def approximate_hours_on_type(self):
        return int(self.__pilot_total_hours * self.__pilot_percent_hours_on_type / 100)


class IncidentCollection(dict):  # extends dict  # no need to reimplement the initializer
    # dict.__init_() is sufficient
    # key:report_id
    # value:Incident
    def values(self):
        for report_id in self.keys():  # call __iter__
            yield self[report_id]

    def items(self):
        for report_id in self.keys():  # call __iter__K
            yield (report_id, self[report_id])

    def __iter__(self):
        for report_id in sorted(super().keys()):  # sorted
            yield report_id

    keys = __iter__()

    def export_pickle(self, filename, compress=False):
        """
        write the IncidentsCollections to file
        :param filename:
        :param compress: gzip or not
        :return: success or not
        """

        # the pickled data is self, a dict.
        # the pickle module is smart enough to be able to save objects of most custom classes without us
        # needing to intervene
        fh = None
        try:
            if compress:
                fh = gzip.open(filename, "wb")  # gzip compression, write binary
            else:
                fh = open(filename, "wb")  # write binary
            pickle.dump(self, fh,
                        pickle.HIGHEST_PROTOCOL)  # write file with pickle, HIGHEST_PROTOCOL, a compact binary pickle format
            return True
        except(EnvironmentError, pickle.PickleError) as err:
            print("{0}: export error: {1}".format(os.path.basename(sys.argv[0]), err))
        finally:
            if fh is not None:
                fh.close()  # close the file

    def import_pickle(self, filename):
        """
        read IncidentsCollections file

        :param filename:
        :return: success or not
        """
        fh = None
        try:
            fh = open(filename, "rb")  # read binary
            magic = fh.read(len(GZIP_MAGIC))  # read the first two bytes
            # if these btyes are the same as the gzip magic number,
            # close the file and create a new file object using the gzip.open() function
            if magic == GZIP_MAGIC:
                fh.close()
                fh = gzip.open(filename, "rb")
            else:  # the file is not compressed
                # file poointer to the beginning of the file
                fh.seek(0)
            # we can't assign to self since that would wipe out the IncidentCollection object
            # that is in use so instead we clear all the incidents to make the dictionary empty
            self.clear()
            # populate the dictionary with all the incidents from the IncidentCollection dictionary
            # loaded from the pickle
            self.update(pickle.load(fh))
            return True
        except (EnvironmentError, pickle.UnpicklingError) as err:
            print("{0}: import error: {1}".format(os.path.basename(sys.argv[0]), err))
            return False
        finally:
            if fh is not None:
                fh.close()

    def export_binary(self, filename, compress=False):
        def pack_string(string):  # inner function
            data = string.encode("utf8")
            # to hold a struct format based on the string's length.
            # h: 16-bit signed integer, H: 16-bit unsigned integer
            # <: little-endian
            # >: big-endian
            format = "<H{0}s".format(len(data))
            return struct.pack(format, len(data), data)

        fh = None
        try:
            if compress:
                fh = gzip.open(filename, "wb")
            else:
                fh = open(filename, "wb")
            fh.write(MAGIC)
            fh.write(FORMAT_VERSION)
            for incident in self.values():
                data = bytearray()
                data.extend(pack_string(incident.report_id))
                data.extend(pack_string(incident.airport))
                data.extend(pack_string(incident.aircraft_id))
                data.extend(pack_string(incident.aircraft_type))
                data.extend(pack_string(incident.narrative.strip()))
                data.extend(NumbersStruct.pack(
                    incident.date.toordinal(),
                    incident.pilot_percent_hours_on_type,
                    incident.pilot_total_hours,
                    incident.midair
                ))
                fh.write(data)
            return True
        except EnvironmentError as err:
            print("{0}: export error: {1}".format(os.path.basename(sys.argv[0]), err))
            return False
        finally:
            if fh is not None:
                fh.close()

    def import_binary(self, filename):
        def unpack_string(fh, eof_is_error=True):
            unit16 = struct.Struct("<H")  # little-endian, 16-bit unsigned
            length_data = fh.read(unit16.size)
            if not length_data:  # null
                if eof_is_error:
                    raise ValueError("missing or corrupt string size")
                return None
            length = unit16.unpack(length_data)[0]
            if length == 0:
                return ""
            data = fh.read(length)
            if not data or len(data) != length:
                raise ValueError("missing or corrupt string")
            format = "<{0}s".format(length)
            return struct.unpack(format, data)[0].decode("utf8")

        fh = None
        try:
            fh = open(filename, "rb")  # the file may or may not compressed
            magic = fh.read(len(GZIP_MAGIC))  # read the first four bytes
            if magic == GZIP_MAGIC:
                fh.close()
                fh = gzip.open(filename, "rb")
            else:
                fh.seek(0)
            magic = fh.read(len(MAGIC))
            if magic != MAGIC:  # isn't a binary aircraft incident data file
                raise ValueError("invalid .aib file format")
            version = fh.read(len(FORMAT_VERSION))  # read 2 bytes version number
            if version > FORMAT_VERSION:  # the version is a later one
                raise ValueError("unrecognized .aib file version")
            self.clear()  # empty the dict

            while True:
                report_id = unpack_string(fh, False)
                if report_id is None:
                    break
                data = {}
                data["report_id"] = report_id  # dict add element
                for name in ("airport", "aircraft_id", "aircraft_type", "narrative"):  # set
                    data[name] = unpack_string(fh)
                other_data = fh.read(NumbersStruct.size)
                # NumbersStruct = struct.Struct("<Idi?")
                numbers = NumbersStruct.unpack(other_data)
                data["date"] = datetime.date.fromordinal(numbers[0])
                data["pilot_percent_hours_on_type"] = numbers[1]
                data["pilot_total_hours"] = numbers[2]
                data["midair"] = numbers[3]
                incident = Incident(**data)  # mapping unpacking
                self[incident.report_id] = incident
            return True
        except(EnvironmentError, ValueError, IndexError, IncidentError) as err:
            print("{0}: import error: {1}".format(os.path.basename(sys.argv[0]), err))
        finally:
            if fh is not None:
                fh.close()

    def export_text(self, filename):
        wrapper = textwrap.TextWrapper(initial_indent="    ", subsequent_indent="    ")  # textWrap.TextWrap object
        fh = None
        try:
            fh = open(filename, "w", encoding="utf8")
            for incident in self.values():
                narrative = "\n".join(wrapper.wrap(incident.narrative.strip()))
                fh.writable("[{0.report_id}]\n"
                            # !s to force string form, !r to force representational form,
                            # !a to force representational form but only using ascii characters
                            "date={0.date!s}\n"
                            "aircraft_id={0.aircraft_id}\n"
                            "airport={airport}\n"
                            "pilot_percent_hours_on_type={0.pilot_percent_hours_on_type}\n"
                            "pilot_total_hours={0.pilot_total_hours}\n"
                            "midair={0.midair:d}\n"  # bool as integer
                            ".NARRATIVE_START.\n"
                            "{narrative}\n"
                            ".NARRATIVE_END.\n"
                            "\n".format(incident, airport=incident.airport.strip(), narrative=narrative)
                            )
                return True
        except EnvironmentError as err:
            print("{0}: export error: {1}".format(os.path.basename(sys.argv[0]), err))
        finally:
            if fh is not None:
                fh.close()
