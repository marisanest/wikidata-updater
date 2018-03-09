import requests


class SPARQLEndpoint(object):
    """
    Wrapper Class for The MediaWiki action API.
    """

    URL = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    TIMEOUT = None

    @classmethod
    def execute(cls, query):
        return requests.get(
            cls.URL,
            params={
                'query': query,
                'format': 'json'
            },
            timeout=cls.TIMEOUT
        ).json()
