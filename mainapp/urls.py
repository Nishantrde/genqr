from django.urls import path
from .views import *

urlpatterns = [
    path("", index),
    path('visit/<uuid:uuid>/', visit, name='show_data'),

]
