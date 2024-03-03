python manage.py makemigrations Account_app
python manage.py makemigrations GearBox_app
python manage.py makemigrations Appointment_app
python manage.py migrate
python manage.py migrate --database=gss_db
@REM python manage.py createsuperuser