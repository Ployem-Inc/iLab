"""
ilab apps
"""
from django.contrib import admin
from .models.python import Python
from .models.javascript import Javascript

admin.site.register(Python)
admin.site.register(Javascript)
