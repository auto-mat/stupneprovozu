import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

from tsk.models import Provoz 

from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

def django_import():
    from django.core.paginator import Paginator
    paginator = Paginator(Provoz.objects.all(), 1000)

    for page in range(1, paginator.num_pages + 1):
        print 'Loading page (1000 objs) no.', page
        for p in paginator.page(page).object_list:
            doc = {
                'location': {'name': p.location.name, 'geo': {'lat': 0, 'lon': 0}},
                'timestamp': p.time_start,
                'traffic': p.level
            }
            res = es.index(index="traffic", doc_type='traffic_report', id=p.id, body=doc)
            #print(res['created'])

def search():
    es.indices.refresh(index="traffic")

    res = es.search(index="traffic", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print hit
        #print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

django_import()
#search()
