"""
ilab url patterns
"""
from django.urls import path, re_path
from . import views
from . import consumers

urlpatterns = [
]

websocket_urlpatterns = [
    re_path(r'ws/api/ilab/python/$', consumers.PythonConsumer.as_asgi(), name="python")
]