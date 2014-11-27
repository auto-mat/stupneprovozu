import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

import datetime
import json
import logging
import urllib
from django.conf import settings

from tsk.models import Lokace, Provoz

logger = logging.getLogger(__name__)

logger.info('Import started at %s' % datetime.datetime.now())

indata = urllib.urlopen(settings.TSK_URL)
data = json.load(indata)

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
    except Exception as e:
        logger.error('Error parsing TSK data: %s' % i)
        logger.error(e)

logger.info('Import finished at %s' % datetime.datetime.now())

