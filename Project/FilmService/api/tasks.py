from datetime import datetime, timedelta

import requests
from django_q.models import Schedule

from .models import Film

# Update all films
# Requests the FilmService to update all films in the database


def update_all_films():
    print("Updating all films", flush=True)

    for film in Film.objects.all():
        response = requests.put(f'http://localhost:8001/update/{film.id}/')

    # Update next run time
    schedule = Schedule.objects.get(pk=1)
    schedule.next_run = ((datetime.utcnow() + timedelta(minutes=15)
                          ).replace(microsecond=0).isoformat() + 'Z')
    schedule.save()