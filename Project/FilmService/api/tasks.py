from django_q.tasks import schedule
from django_q.models import Schedule
from .models import Film
import requests

# Define the task function


def update_all_films():
    print("Updating all films", flush=True)
    for film in Film.objects.all():
        response = requests.put(f'http://localhost:8001/update/{film.id}/')


# Check if the schedule already exists
if not Schedule.objects.filter(func='api.tasks.update_all_films', schedule_type='I').exists():
    
    # Create a new schedule if one doesn't already exist
    schedule('api.tasks.update_all_films', schedule_type='I', minutes=10)

