import json
import logging

from item import WikidataItem


class Import(object):

    def __init__(self, json_file):
        with open(json_file) as file:
            self.json = json.load(file)

    def start(self):
        for item_values in self.json:
            WikidataItem(item_values['id']).update(item_values)
            logging.info(' Item with id = ' + item_values['id'] + ' updated.')

