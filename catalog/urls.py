from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from catalog.views import (ProductListView, ProductCreateView, UserContactsCreateView,
                           ProductDetailView, MyContactListView, BlogListView, BlogCreateView,
                           BlogUpdateView, BlogDeleteView, BlogDetailView, ProductUpdateView, CategoryListView)

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='homepage'),
    path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='view_product'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('create/', never_cache(ProductCreateView.as_view()), name='product_create'),

    path('category', CategoryListView.as_view(), name='category'),

    path('blog', BlogListView.as_view(), name='blog'),
    path('blog/create/', never_cache(BlogCreateView.as_view()), name='blog_create'),
    path('blog/update/<slug:slug>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<slug:slug>/', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/view/<slug:slug>/', BlogDetailView.as_view(), name='view_blog'),

    path('usercontacts/', UserContactsCreateView.as_view(), name='user_contacts'),
    path('mycontact/', MyContactListView.as_view(), name='my_contact'),
]
