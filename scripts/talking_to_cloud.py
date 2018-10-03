import getpass
import random
import json
from elasticsearch import Elasticsearch
from prettytable import PrettyTable


input('\nWelcome to a quick, cheesy tutorial to help getting started with Elasticsearch! Hit enter to begin.  ')

print('\nLet\'s set up your Elasticsearch connection...')
# Gather connection information
user = input('Username: ')
password = getpass.unix_getpass()
host = input('A connection URL (e.g. myhost:9200): ')


# Create a connection to your Elasticsearch cluster
elasticsearch_client = Elasticsearch(
    hosts=[
        '{}:{}@e{}'.format(user, password, host)
    ],
    use_ssl=True,
    verify_certs=True
)


# Verify that we can interact with the Elasticsearch cluster
if elasticsearch_client.ping() is True:
    print('\n+1... Yay, a successful call to your Elasticsearch client\'s .ping() method!  ')


input('\nHit enter to see the indices that exist on your Elasticsearch cluster...  ')


# See which indices exist on your cluster
indices = elasticsearch_client.cat.indices('*', v=True, format='json')
fields = set()
indices_table = PrettyTable()
indices_table.field_names = list(indices[0].keys())
[indices_table.add_row(list(r.values())) for r in indices]
print(indices_table)


input('\nHit enter to start adding some data...  ')
my_index = input('Data goes in an index. What\'s the name of yours?  ')
for i in range(5):
    elasticsearch_client.index(my_index, doc_type='record', body=dict(number_field=random.randint(1,100)))


input('\nAll done! Hit enter to see the list of indices again. Note your new index is there!  ')


# See which indices exist on your cluster
indices = elasticsearch_client.cat.indices('*', v=True, format='json')
fields = set()
indices_table = PrettyTable()
indices_table.field_names = list(indices[0].keys())
[indices_table.add_row(list(r.values())) for r in indices]
print(indices_table)


input('\nHit enter to do an aggregation query on the field named "number_field" in your new index')
query = {
  "query": {"match_all": {}},
  "size": 0,
  "aggs": {
    "number_stats": {
      "extended_stats": {
        "field": "number_field"
      }
    }
  }
}
print('\nThe query is:')
print(json.dumps(query, indent=2))
response = elasticsearch_client.search(index=my_index, doc_type='record', body=query)
input('Hit enter to see the response...  ')
print(json.dumps(response, indent=2))
print('As you can see, the minimum value of "number_field" is {}, the maximum value is {}, and so on.'.format(
    response['aggregations']['number_stats']['min'],
    response['aggregations']['number_stats']['max']
))


cleanup = input('\nWould you like to remove data from your cluster that was added in this demo? (y/n)  ')
if cleanup == 'y':
    elasticsearch_client.indices.delete(my_index)

print('\nYou have now seen how to connect to an Elasticsearch cluster from Python, view existing indices, auto-creat a '
      'new index, index documents, and do some numeric aggregations.')
print('-  Did you read the source code? You should!')
print('-  Play around with Python and Kibana to add, remove, visualize, and analyze your data')
