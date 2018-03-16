import datetime
import csv
import json
import re
import logging

from query import FindIdQuery


class CSVParser(object):
    """
    Class for parsing csv.
    """

    REGEX_IS_ID = re.compile('^Q[1-9][0-9]*$')
    REGEX_IS_DATE = re.compile('^\+[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$')
    REGEX_IS_ONLY_YEAR = re.compile('^\+[12][0-9]{3}-00-00T00:00:00Z$')
    REGEX_PARSE_YEAR = re.compile('^\+([12][0-9]{3})')

    INSTANCE_OF_ITEM_FOR_PROPERTY = {
        'P734': 'Q101352',
        'P735': 'Q202444',
        'P1559': 'Q82799',
        'P19': 'Q515'
    }

    federal_court_dataset_ids = None

    def __init__(self, csv_path, step_size, buffer=False, buffer_path=None):
        with open(csv_path, newline='') as file:
            self.csv = [_ for _ in csv.reader(file, delimiter=';', quotechar='"')]
        self.header = self.csv[0][1:]
        self.data = self.csv[1:]
        self.step_size = step_size
        self.parsed_data = None

        if buffer and not buffer_path:
            raise ValueError(' If buffer is set to True, buffer_path has to be set as well.')

        self.buffer = buffer
        self.buffer_path = buffer_path

    def parse_csv(self):

        self.parsed_data = []

        for line in self.data:
            self.parsed_data.append(self.parse_line(line))

            if self.buffer:
                self.save_as_json(self.buffer_path)

            logging.info(' Line with id = ' + line[0] + ' parsed.')

        return self

    def parse_line(self, line):
        """
        Function to parse a line.

        @param line: line
        @type line: list

        @return: parsed line
        @rtype: dict
        """

        parsed_line = {
            'id': line[0],
            'claims': [],
            'references': self.get_references(line[0])
        }

        if self.header[-1] == 'Beschreibung':
            parsed_line['descriptions'] = {'de': line[-1]}

        _line = line[1:-1] if self.header[-1] == 'Beschreibung' else line[1:]

        for index in range(0, len(_line), self.step_size):

            property, value = self.header[index], _line[index]
            qualifier_ids, qualifier_values = self.header[index + 1:index + self.step_size], _line[
                                                                                             index + 1:index + self.step_size]

            if not self.is_parseable(value) or not self.is_necessary(value, line[0]):
                continue

            try:
                value = self.parse_value(value, property)
            except Exception as exception:
                logging.warning(
                    ' Value = ' + value + ' could not be parsed for property = ' + property + '.',
                    exc_info=exception,
                    stack_info=True
                )
                continue

            claim = {
                'id': property,
                'value': value,
            }

            qualifiers = self.parse_qualifiers(qualifier_ids, qualifier_values)

            if qualifiers:
                claim['qualifiers'] = qualifiers

            parsed_line['claims'].append(claim)

        return parsed_line

    def save_as_json(self, save_path):

        if self.parsed_data is None:
            raise ValueError('data not parsed yet')

        with open(save_path, 'w') as file:
            json.dump(self.parsed_data, file)

    @classmethod
    def parse_value(cls, value, id=None):

        if cls.is_date(value):
            return cls.parse_date(value)

        elif cls.is_id(value) or id is None:
            return value

        else:
            return cls.get_id(id, value)

    @classmethod
    def parse_qualifiers(cls, qualifier_ids, qualifier_values):

        parsed_qualifiers = []

        for index, qualifier_value in enumerate(qualifier_values):

            if cls.is_parseable(qualifier_value):
                qualifier_value = cls.parse_value(qualifier_value)

                parsed_qualifiers.append(
                    {
                        'id': qualifier_ids[index],
                        'value': qualifier_value
                    }
                )

        return parsed_qualifiers

    @classmethod
    def get_references(cls, id):

        if id in cls.get_federal_court_dataset_ids():

            parsed_references = [
                {
                    'id': 'P854',
                    'value': 'http://www.richter-im-internet.de'
                },
                {
                    'id': 'P248',
                    'value': 'Q32961325'
                }
            ]
        else:
            parsed_references = [
                {
                    'id': 'P143',
                    'value': 'Q48183'
                }
            ]

        parsed_references.append(
            {
                'id': 'P813',
                'value': cls.parse_date(datetime.datetime.now())
            }
        )

        return parsed_references

    @classmethod
    def parse_date(cls, date):
        """
        Helper function to parse a date.

        @param date: date
        @type date: string, datetime
        @param: only_year: if only year should parsed
        @type: bool

        @return: The parsed date
        @rtype: tuple
        """

        if not isinstance(date, datetime.datetime):

            if cls.REGEX_IS_ONLY_YEAR.match(date):
                return cls.REGEX_PARSE_YEAR.match(date).group(1), None, None

            date = datetime.datetime.strptime(date, '+%Y-%m-%dT%H:%M:%SZ')

        return date.year, date.month, date.day

    @classmethod
    def is_necessary(cls, value, id):
        return not (not cls.is_date(value) and not cls.is_id(value) and id in cls.get_federal_court_dataset_ids())

    @classmethod
    def is_parseable(cls, value):
        return value != '##' and value != '' and value is not None

    @classmethod
    def is_date(cls, value):
        return cls.REGEX_IS_DATE.match(value)

    @classmethod
    def is_id(cls, value):
        return cls.REGEX_IS_ID.match(value)

    @classmethod
    def get_federal_court_dataset_ids(cls):

        if cls.federal_court_dataset_ids is None:
            cls.federal_court_dataset_ids = set()

            with open('../data/positionen.csv', newline='') as file:
                for row in [_ for _ in csv.reader(file, delimiter=';', quotechar='"')][1:]:
                    cls.federal_court_dataset_ids.add(row[0])

        return cls.federal_court_dataset_ids

    @classmethod
    def get_id(cls, property, label):
        """
        Function to search the id for an item with the label given label.
        The item sould fit as an value for the given property.

        @param property: property
        @type property: string
        @param label: label
        @type label: string

        @return: The matching id
        @rtype: string
        """

        if property not in cls.INSTANCE_OF_ITEM_FOR_PROPERTY:
            raise ValueError(
                'property must be one of: ' + ', '.join(
                    cls.INSTANCE_OF_ITEM_FOR_PROPERTY.keys()) + ' got ' + property)

        return FindIdQuery(cls.INSTANCE_OF_ITEM_FOR_PROPERTY[property], label).execute().extract()
