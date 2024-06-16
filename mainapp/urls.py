from django.urls import path
from .views import *

urlpatterns = [
    path("", index),
    path("custom", custom),
    path('visit/<uuid:uuid>', visit, name='show_data'),
    path('file/<uuid:uuid>', visit_file, name='show_file'),
    path('upload_files', upload_files)

]
