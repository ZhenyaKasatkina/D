from django.shortcuts import render
from django.views.generic import ListView

# from catalog.management.commands.fill import Command
from catalog.models import MyContact, Product, Category


def homepage(request):
    if request.method == 'POST':
        # print(request.POST)
        # print(request.POST.get('category'))
        # print(f"{product_name}, {price}, {preview} ({category}): {description}")

        Product.objects.create(
            product_name=request.POST.get('product_name'),
            category_id=request.POST.get('category'),
            price=request.POST.get('price'),
            preview=request.FILES.get('preview'),
            description=request.POST.get('description')
        )

    # five_latest_products = Command.json_read_products()[-5:]  #ДЗ 20.1
    # for prod in five_latest_products:
    #     print(prod["fields"]["product_name"])

    context = {'object_list': Product.objects.all(),
               'title': 'Главная сраница Вкусняшек',
               'category_list': Category.objects.all()}
    return render(request, 'catalog/homepage.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name} ({phone}): {message}")

    context = {'object': MyContact.objects.get(),
               'title': 'Контакты'}
    return render(request, 'catalog/contacts.html', context)


def product(request, pk):
    if pk != 1:
        previous_page = Product.objects.get(pk=(pk - 1))
    else:
        previous_page = Product.objects.get(pk=1)
    if pk != Product.objects.count():
        next_page = Product.objects.get(pk=(pk+1))
    else:
        next_page = Product.objects.get(pk=(Product.objects.count()))

    context = {'object': Product.objects.get(pk=pk),
               'title': 'Вот что ты выбрал',
               'previous_page': previous_page,
               'next_page': next_page
               }
    # print(context['previous_page'])
    return render(request, 'catalog/product.html', context)
