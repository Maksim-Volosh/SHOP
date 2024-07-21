from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart, name='cart'),
    path('ajax/add', cart_add, name='cart_add'),
    path('ajax/delete', cart_delete, name='cart_delete'),
    path('ajax/update', cart_update, name='cart_update'),
]
