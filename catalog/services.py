from django.core.cache import cache

from catalog.models import Category
from config.settings import CACHE_ENABLED


def get_category_from_cache():
    """
    Если категории есть, то берем из в кеш,
    если нет в кеш - то из БД
    """
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = 'category_list'
    categories = cache.get(key)
    if categories is not None:
        return categories
    categories = Category.objects.all()
    cache.get(key)
    return categories
