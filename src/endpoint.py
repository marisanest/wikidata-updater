import requests


class SPARQLEndpoint(object):
    """
    Wrapper Class for The MediaWiki action API.
    """

    URL = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'

    @staticmethod
    def execute(query):
        return requests.get(
            SPARQLEndpoint.URL,
            params={
                'query': query,
                'format': 'json'
            }
        ).json()
