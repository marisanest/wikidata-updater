# from helper import Helper
import datetime
import csv


class DataParser:
    """
    Class for parsing data.
    """

    def __init__(self, file_path, site):
        with open(file_path, newline='') as file:
            self.data = [_ for _ in csv.reader(file, delimiter=';', quotechar='"')]
        self.header = self.data[0]
        self.data = self.data[1:]
        self.site = site

    def parse_data(self):
        return [self.parse_line(line) for line in self.data]

    def parse_line(self, line):
        """
        Function to parse one line.

        @param line: The line which should be parsed.
        @type line: list

        @return: The parsed data
        @rtype: dict
        """

        parsed_line = {
            'id': line[0],
            'label': {'de': line[-2]},
            'properties': {}
        }

        if line[-1] == '0':
            parsed_line['source'] = {'P854': 'http://www.richter-im-internet.de',
                                     'P248': 'Q32961325',
                                     'P813': datetime.datetime.now()}
        elif line[-1] == '1':
            parsed_line['source'] = {'P143': 'Q48183',
                                     'P813': datetime.datetime.now()}

        _line = line[1:-2]

        for index in range(0, len(_line), 4):
            if _line[index] == '##' or _line[index] == '' or _line[index] == None:
                continue

            # if _line[index].startswith('+'):
            #    _line[index] = 'DATE'  # DataParser.parse_date(line[index])
            # elif not _line[index].startswith('Q'):
            #    _line[index] = 'LITERAL'  # Helper.qid_for(self.site, statement[0], 'given_name')

            parsed_line['properties'][self.header[index + 1]] = {'value': _line[index]}

            if _line[index + 1] != '##' and _line[index + 1] != '' and _line[index + 1] != None:
                parsed_line['properties'][self.header[index + 1]]['qualifiers'] = {'P580': _line[index + 1]}

            if _line[index + 2] is not '##' and _line[index + 2] is not '' and _line[index + 2] is not None:
                parsed_line['properties'][self.header[index + 1]]['qualifiers']['P582'] = _line[index + 2]

        return parsed_line

    @staticmethod
    def parse_date(date):
        """
        Helper function to parse a date.

        @param year: The year which should be parsed.
        @type year: string
        @param month: The month which should be parsed.
        @type month: string
        @param day: The day which should be parsed.
        @type day: string

        @return: The parsed date
        @rtype: array
        """
        pass
