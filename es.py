import sys
from elasticsearch import Elasticsearch
from datetime import datetime


elastic_pass = "FE0Yrg2pU5jxf0Ea7V7a5d5l"
elastic_endpoint = "https://cs172-project-ad1cfb.es.eastus2.azure.elastic-cloud.com:9243"

esConn = Elasticsearch(
    cloud_id="cs172-project:ZWFzdHVzMi5henVyZS5lbGFzdGljLWNsb3VkLmNvbTo5MjQzJDQzYTcyYzM3YTQ3OTQyNWZiMGVhZDRmZDRlMDE3ZWQyJGEzNjhkZWExOTBkZjRiM2FiNmRlN2E3ZWJkMmQ0M2Y2", http_auth=("elastic", "FE0Yrg2pU5jxf0Ea7V7a5d5l"))

# doc = {
#     "url": "https://ucsd.edu",
#     "page_title": "University of California San Diego",
#     "text": "<p>Top public university in the nation for contributions to social mobility, research and public service.</p>",
#     "timestamp": datetime.now(),
#     "author": ""
# }


def uploadDoc(doc):
    try:
        res = esConn.index(index="edusite", id=1, body=doc)
        print(res)
    except ConnectionError as err:
        print("Unexpected error: {}".format(err))

# def bulkLoad(docs):