from django.contrib import admin

from catalog.models import Category, Product, MyContact


@admin.register(MyContact)
class MyContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_name', 'country', 'inn', 'address', 'email', 'logo',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('product_name', 'description',)
