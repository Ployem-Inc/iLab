# Generated by Django 3.2.8 on 2022-07-22 20:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ilab', '0005_auto_20220722_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='javascript',
            name='id',
            field=models.UUIDField(default=uuid.UUID('cc190b98-d387-48eb-ae87-a0131520443c'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='javascript',
            name='interpreter_path',
            field=models.CharField(default='/Users/king_ahmed1421/Simba/Ployem/backend/ilab/models/interpreters/cc190b98-d387-48eb-ae87-a0131520443c.js', max_length=676),
        ),
        migrations.AlterField(
            model_name='python',
            name='id',
            field=models.UUIDField(default=uuid.UUID('af9de431-2475-46af-ae9f-440848a2272d'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='python',
            name='interpreter_path',
            field=models.CharField(default='/Users/king_ahmed1421/Simba/Ployem/backend/ilab/models/interpreters/af9de431-2475-46af-ae9f-440848a2272d.py', max_length=676),
        ),
    ]