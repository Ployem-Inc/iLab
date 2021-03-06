# Generated by Django 3.2.8 on 2022-07-22 19:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ilab', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Javascript',
            fields=[
                ('docker_image', models.CharField(max_length=26)),
                ('id', models.UUIDField(default=uuid.UUID('6d9de395-c197-4fa3-b562-1d1f90e7678d'), editable=False, primary_key=True, serialize=False, unique=True)),
                ('interpreter_path', models.CharField(default='/Users/king_ahmed1421/Simba/Ployem/backend/ilab/models/interpreters/6d9de395-c197-4fa3-b562-1d1f90e7678d.js', max_length=676)),
            ],
        ),
        migrations.AlterField(
            model_name='python',
            name='id',
            field=models.UUIDField(default=uuid.UUID('2aee57da-d8ab-4047-a764-310a5327a365'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='python',
            name='interpreter_path',
            field=models.CharField(default='/Users/king_ahmed1421/Simba/Ployem/backend/ilab/models/interpreters/2aee57da-d8ab-4047-a764-310a5327a365.py', max_length=676),
        ),
    ]
