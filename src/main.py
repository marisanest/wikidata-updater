from parser import CSVParser
from importer import Import

CSVParser('../data/positionen.csv', 5).parse_csv().save_as_json('../data/positionen.json')
CSVParser('../data/import.csv', 3).parse_csv().save_as_json('../data/import.json')

Import().start('../data/positionen.json')
Import().start('../data/import.json')

