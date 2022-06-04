# Generated by Django 3.2.8 on 2022-06-03 07:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Python',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('docker_image', models.CharField(max_length=26)),
                ('interpreter_path', models.CharField(default='/Users/king_ahmed1421/Simba/Ployem/backend/ilab/models/<django.db.models.fields.UUIDField>.py', max_length=676)),
            ],
        ),
    ]