python mainapp/manage.py makemigrations
python mainapp/manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python mainapp/manage.py shell
python mainapp/manage.py runserver 0.0.0.0:8000
