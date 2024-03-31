from django.shortcuts import render
from django.views.generic import ListView

from catalog.management.commands.fill import Command
from catalog.models import MyContact


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name} ({phone}): {message}")
    return render(request, 'catalog/contacts.html')


def homepage(request):
    five_latest_products = Command.json_read_products()[-5:]
    for product in five_latest_products:
        print(product["fields"]["product_name"])
    return render(request, 'catalog/homepage.html')


class MyContactView(ListView):
    model = MyContact
    template_name = 'contacts.html'
    context_object_name = 'my_contacts'
