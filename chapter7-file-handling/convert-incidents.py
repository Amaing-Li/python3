import datetime


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
