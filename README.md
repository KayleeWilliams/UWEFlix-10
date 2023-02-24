# UWEFlix-10
Group project for DESD @ UWE
## How to run
1. Clone the repository
2. Run the command `docker-compose up --build` in the folder named project directory
3. If 1st run see the next section as you need to do the command `python manage.py migrate`
4. Navigate to `localhost:8000` in your browser

## How to make migrations
Run the command `docker-compose exec web bash` in the root directory

Now you can run the following commands in the terminal:
- `python manage.py migrate`
- `python manage.py makemigrations`

