from endpoint import SPARQLEndpoint


class Query(object):

    QUERY = None

    def __init__(self, query):
        self.endpoint = SPARQLEndpoint()
        self.query = query
        self.response = None

    def execute(self):
        self.response = self.endpoint.execute(self.query)
        return self

    def extract(self):
        raise NotImplementedError


class FindIdQuery(Query):

    QUERY = '''
        SELECT DISTINCT ?item
        WHERE {
            ?item wdt:P31/wdt:P279* wd:## ; rdfs:label ?itemLabel .
            FILTER REGEX(?itemLabel, "^##$") .  
        }
    '''

    def __init__(self, instance_of, label):
        super().__init__(self.__class__.QUERY
                         .replace('##', instance_of, 1)
                         .replace('##', label))

    def extract(self):
        if self.response is None:
            raise ValueError('response not requested yet.')
        return [binding['item']['value'] for binding in self.response['results']['bindings']][0]\
            .replace('http://www.wikidata.org/entity/', '')
