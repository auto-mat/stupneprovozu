import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

import json
import logging
from tsk.models import Lokace, Provoz

logger = logging.getLogger(__name__)

indata = open('stupneprovozu.json').read()
data = json.loads(indata)

for i in data['results']:
    try:
        lokace, created = Lokace.objects.get_or_create(name=i['location'])
        provoz, created = Provoz.objects.get_or_create(
            ident=i['id'],
            location=lokace,
            level=i['level'],
            time_generated=i['timeGenerated'],
            time_start=i['timeStart'],
            time_stop=i['timeStop'],
        )
    except Exception,e:
        logger.exception('Error parsing TSK data: %s' % i)

