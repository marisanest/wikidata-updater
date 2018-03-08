from helper import Helper
import datetime
import csv
import json
import re


class CSVParser:
    """
    Class for parsing csv.
    """

    REGEX_ID = re.compile('^Q[1-9][0-9]*$')
    REGEX_DATE = re.compile('^\+[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$')

    def __init__(self, csv_path='../data/import.csv', json_path='../data/import.json'):
        with open(csv_path, newline='') as file:
            self.csv = [_ for _ in csv.reader(file, delimiter=';', quotechar='"')]
        self.header = self.csv[0][1:]
        self.data = self.csv[1:]
        self.parsed_data = None
        self.json_path = json_path

    def parse_csv(self):
        self.parsed_data = [self.parse_line(line) for line in self.data]
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
            'label': {'de': line[-2]},
            'properties': []
        }

        # todo: fragen ob alles nur FS50 daten betrifft
        if line[-1] == '0':
            parsed_line['source'] = {'P854': 'http://www.richter-im-internet.de',
                                     'P248': 'Q32961325'}
        elif line[-1] == '1':
            parsed_line['source'] = {'P143': 'Q48183'}

        if line[-1] == '0' or line[-1] == '1':
            parsed_line['source']['P813'] = self.__class__.parse_date(datetime.datetime.now())

        _line = line[1:-2]

        for index in range(0, len(_line), 4):
            if _line[index] == '##' or _line[index] == '' or _line[index] is None:
                continue

            if self.__class__.REGEX_DATE.match(_line[index]):
                _line[index] = CSVParser.parse_date(line[index])
            elif not self.__class__.REGEX_ID.match(_line[index]):
                try:
                    _line[index] = Helper.id_for(self.header[index], _line[index])
                except:
                    print('WARNING: label=' + _line[index] + ' could not be parsed for property=' + self.header[index])
                    continue

            parsed_property = {
                'id': self.header[index],
                'value': _line[index],
            }

            parsed_qualifiers = self.parse_qualifiers([_line[index + 1], _line[index + 2]])
            if parsed_qualifiers:
                parsed_property['qualifiers'] = parsed_qualifiers

            parsed_line['properties'].append(parsed_property)

        return parsed_line

    def parse_qualifiers(self, qualifiers):
        properties = ['P580', 'P582']
        return [
            {
                'id': properties[index],
                'value': CSVParser.parse_date(qualifier)
            } for index, qualifier in enumerate(qualifiers)
            if qualifier != '##' and qualifier != '' and qualifier is not None
        ]

    def save_as_json(self):
        if self.parsed_data is None:
            raise ValueError('data not parsed yet')
        with open(self.json_path, 'w') as file:
            json.dump(self.parsed_data, file)

    @staticmethod
    def parse_date(date):
        """
        Helper function to parse a date.

        @param date: date
        @type date: string, datetime

        @return: The parsed date
        @rtype: tuple
        """

        if not isinstance(date, datetime.datetime):
            date = datetime.datetime.strptime(date, '+%Y-%m-%dT%H:%M:%SZ')

        return date.year, date.month, date.day
