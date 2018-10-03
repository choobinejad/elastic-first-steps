import csv
import getpass
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def clean_types(record: dict) -> dict:
    """
    Python's csv reader makes everything a string. Lame. Map fields to their desired type.

    :param record: A dict that needs to be coerced to have the intended types for Elasticsearch
    :return: The prepared dict
    """
    type_mapping = dict(
        geonameid=str,
        latitude=float,
        longitude=float,
        population=int,
        elevation=float
    )
    return {
        k: type_mapping.get(k, str)(v) for k, v in record.items() if v != ''
    }


def generate_documents(records: list):
    """
    A generator which yields documents to the bulk indexing helper for Elasticsearch.

    :param records: An iterable of dict
    """
    for record in records:
        source = clean_types(dict(zip(headers, record)))
        if source.get('latitude') is not None and source.get('longitude') is not None:
            source['location'] = [source['longitude'], source['latitude']]
        yield dict(
            _op_type='index',
            _index='geonames',
            _type='record',
            _id=source['geonameid'],
            _source=source
        )


print('\nLet\'s set up your Elasticsearch connection...')
# Gather connection information
user = input('Username: ')
password = getpass.unix_getpass()
host = input('A connection URL (e.g. myhost:9200): ')


# Create a connection to your Elasticsearch cluster
elasticsearch_client = Elasticsearch(hosts=['{}:{}@e{}'.format(user, password, host)], use_ssl=True, verify_certs=True)

# Check for an existing 'geonames' index
if elasticsearch_client.indices.exists('geonames') is True:
    raise AttributeError('The `geonames` index already exists. Stopping script for safety!')

# If mapping doesn't already exist, create it with the intended types.
elasticsearch_client.indices.create(
    'geonames',
    body={
      "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
      },
      "mappings": {
        "record": {
          "properties": {
            "geonameid": {"type": "integer"},
            "elevation": {"type": "integer"},
            "population": {"type": "integer"},
            "latitude": {"type": "scaled_float", "scaling_factor": 100000},
            "longitude": {"type": "scaled_float", "scaling_factor": 100000},
            "location": {"type": "geo_point"}
          }
        }
      }
    }
)


# Now parse some data!
headers = [
    'geonameid', 'name', 'asciiname', 'alternativenames', 'latitude', 'longitude', 'feature_class', 'feature_code',
    'country_code', 'cc2', 'admin1_code', 'admin2_code', 'admin3_code', 'admin4_code', 'population', 'elevation',
    'dem', 'timezone', 'modification_date'
]

with open('./sample_data/geonames_is_sample.txt', 'r') as f:
    data = list(csv.reader(f, delimiter='\t'))


indexing_results = bulk(elasticsearch_client, generate_documents(data))

print('Done!')

