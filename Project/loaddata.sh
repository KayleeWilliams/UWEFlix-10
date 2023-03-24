# Migrate main app
python manage.py migrate

# Load the data 
python manage.py loaddata tickets_screens.json
python manage.py loaddata films.json
python manage.py loaddata showings.json
python manage.py loaddata groups.json
python manage.py loaddata permissions.json
python manage.py loaddata users.json

# Migrate the FilmService 
cd FilmService
python manage.py migrate

# Load the data
python manage.py loaddata schedule.json
