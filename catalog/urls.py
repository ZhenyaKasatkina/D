from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (ProductListView, ProductCreateView, UserContactsCreateView,
                           ProductDetailView, MyContactListView, BlogListView, BlogCreateView,
                           BlogUpdateView, BlogDeleteView, BlogDetailView)

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='homepage'),
    path('usercontacts/', UserContactsCreateView.as_view(), name='user_contacts'),
    path('mycontact/', MyContactListView.as_view(), name='my_contact'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='view_product'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('blog', BlogListView.as_view(), name='blog'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/update/<slug:slug>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<slug:slug>/', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/view/<slug:slug>/', BlogDetailView.as_view(), name='view_blog'),
]
