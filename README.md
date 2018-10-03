## So you'd like to _elastic_?

Elasticsearch is a distributed search and analytics system with lots of use cases. You can learn lots about
Elasticsearch in [the docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/_basic_concepts.html),
or dive right in to the [query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html).
There's also a nice 
[intro webinar](https://www.elastic.co/webinars/getting-started-elasticsearch?blade=video&hulk=youtube). Since this
quick tour uses Python, you'll also want to have the 
[Python Elasticsearch client docs](https://elasticsearch-py.readthedocs.io/en/master/) handy.


## Tutorial Environment
This tutorial assumes that you're using Python 3.x, that you've cloned this Git repo, and that you've run
`pip install -r requirements.txt --upgrade` from this project directory.

Feel free to open issues if (when) you find any!


##Enough chit-chat. Agenda time!

 1. Use Elastic Cloud to spin up an Elasticsearch cluster
 1. Connect to the Elasticsearch cluster and explore a couple of its APIs
 1. Load some data from a sample .csv file
 1. Explore the _/\_search_ API
 1. Finally, we'll see some of the visualization/dashboard capabilities built into the Kibana application.
 

## How to Cloud

Head over to [Elastic Cloud](https://www.elastic.co/cloud/elasticsearch-service/signup). Sign up. Use the free trial. 
Create a `deployment`. The web UI will show you progress on spinning up your cluster, and it will provide you with
some important information: your Elasticsearch URL, your Kibana URL, and your username/password.
Keep these things handy.

Now is also a good time to say that you can run Elasticsearch and Kibana for free on your own machine. While it's not
hard to get started, that's outside the scope of this tutorial. Refer to 
[Installation](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html) to get started
if you want to run the software locally.


## Talking to Cloud
Read (the source!) and run `python ./scripts/talking_to_cloud.py` from your terminal. It'll ask for your connection 
credentials and walk through an interactive-ish couple of quick API calls to your Elasticsearch cluster. This script
is heavily annotated to support the interactive experience.


## Have some geo fun
Read and run `python ./scripts/index_geonames.py`. It indexes a sample of data from 
[Geonames](http://download.geonames.org/export/dump/) for Iceland. (The sample being in `./sample_data`.) It's a
drop-in replacement for the actual geonames files, so you could extend this demo to index much more data into your
Elasticsearch cluster. (Hint: if you want to index more data, check out the docs for 
[bulk helpers](https://elasticsearch-py.readthedocs.io/en/master/helpers.html#bulk-helpers).) When you're done in
Python, head over to your Kibana instance and set up some maps. How is `population` distributed `geographically` in
Iceland?