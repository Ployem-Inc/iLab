# Generated by Django 3.2.8 on 2022-07-22 20:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ilab', '0006_auto_20220722_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='javascript',
            name='id',
            field=models.UUIDField(default=uuid.UUID('414035be-d379-47fb-ab47-fc3f714746d1'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='javascript',
            name='interpreter_path',
            field=models.CharField(default='/Users/king_ahmed1421/Simba/Ployem/backend/ilab/models/interpreters/414035be-d379-47fb-ab47-fc3f714746d1.js', max_length=676),
        ),
        migrations.AlterField(
            model_name='python',
            name='id',
            field=models.UUIDField(default=uuid.UUID('8efad9c0-6157-46e9-b84c-9dba1605e845'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='python',
            name='interpreter_path',
            field=models.CharField(default='/Users/king_ahmed1421/Simba/Ployem/backend/ilab/models/interpreters/8efad9c0-6157-46e9-b84c-9dba1605e845.py', max_length=676),
        ),
    ]
