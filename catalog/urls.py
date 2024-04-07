from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import homepage, contacts, product

app_name = CatalogConfig.name

urlpatterns = [
    path('', homepage, name='homepage'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:pk>', product, name='product')

]
