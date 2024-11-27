echo "Building Project Packages..."
pip install -r requirements.txt

echo "Migrating Database..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting Static Files..."
python manage.py collectstatic --no-input