from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

app_name = 'shop'

urlpatterns = [
    path('', products_all, name='products'),
    path('<slug:slug>/', product_detail, name='product_detail'),
    path('search/<slug:slug>/', category_list, name='category_list'),
]
