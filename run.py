import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

import json
from tsk.models import Lokace, Provoz

indata = open('stupneprovozu.json').read()
data = json.loads(indata)

for i in data['results']:
    lokace, created = Lokace.objects.get_or_create(name=i['location'])
    provoz, created = Provoz.objects.get_or_create(
        ident=i['id'],
        location=lokace,
        level=i['level'],
        time_generated=i['timeGenerated'],
        time_start=i['timeStart'],
        time_stop=i['timeStop'],
    )

