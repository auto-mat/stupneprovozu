import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

from tsk.models import Provoz 

from datetime import datetime

from elasticsearch.helpers import streaming_bulk

from elasticsearch_dsl import DocType, Object, String, GeoPoint, Date, Integer, Float
from elasticsearch_dsl.connections import connections

es = connections.create_connection()

class TrafficReport(DocType):
    location = Object(properties={
        'name': String(fields={'raw': String(index='not_analyzed')}),
        'geo': GeoPoint()
    })
    timestamp = Date()

    class Meta:
        index = 'traffic'

def get_provoz():
    for p in Provoz.objects.all().select_related('location')[:500000].iterator():
        yield {
            'location': {'name': p.location.name, 'geo': {'lat': 0, 'lon': 0}},
            'timestamp': p.time_start,
            'traffic': p.level,
            'cas': float(p.time_start.strftime('%H')) + float(p.time_start.strftime('%M'))/60,
            'den_v_tydnu': p.time_start.weekday(),
            '_id': p.id
        }

def django_import():
    #es.indices.delete(index='traffic', ignore=404)
    #TrafficReport.init()
    i = 0
    for ok, info in streaming_bulk(es, get_provoz(), doc_type='traffic_report', index='traffic'):
        i+= 1
        if i % 1000 == 0:
            print(i, 'dokumentu hotovo')

def search():
    es.indices.refresh(index="traffic")

    res = es.search(index="traffic", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print hit
        #print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

django_import()
#search()
