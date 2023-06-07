import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animer.settings')
django.setup()

from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType
from django.db import connections

# Clear all data in the PostgreSQL database
print("Clearing PostgreSQL data...")
call_command('flush', '--noinput', '--database=default')

# Load data from SQLite into PostgreSQL
print("Loading data from SQLite to PostgreSQL...")
for ct in ContentType.objects.using('sqlite').all():
    model = ct.model_class()
    if model is not None:
        print(f"Transferring {ct.model}...")
        for obj in model.objects.using('sqlite').all():
            obj.pk = None
            obj.save(using='default')

print("Data transfer complete.")