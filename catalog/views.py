from django.core.mail import send_mail
# from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

# from catalog.management.commands.fill import Command
from catalog.models import MyContact, Product, Category, UserContacts, Blog


class ProductListView(ListView):
    model = Product
    extra_context = {'title': 'Главная страница Вкусняшек'}
    paginate_by = 5
    orphans = 4

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['category_list'] = Category.objects.all()
        print(context_data)
        return context_data


class ProductCreateView(CreateView):
    model = Product
    fields = ('product_name', 'category', 'price', 'preview', 'description')
    success_url = reverse_lazy('catalog:homepage')


#     # five_latest_products = Command.json_read_products()[-5:]  #ДЗ 20.1
#     # for prod in five_latest_products:
#     #     print(prod["fields"]["product_name"])


class UserContactsCreateView(CreateView):
    model = UserContacts
    extra_context = {'title': 'Вкусняшка от пользователя'}
    fields = ('name', 'phone', 'email', 'message')
    success_url = reverse_lazy('catalog:homepage')
    print(UserContacts)


class MyContactListView(ListView):
    model = MyContact
    extra_context = {'title': 'Наши Контакты'}


class ProductDetailView(DetailView):
    model = Product
    extra_context = {
        'title': 'Вот что ты выбрал',
    }


class BlogListView(ListView):
    model = Blog
    extra_context = {'title': '???  Оказывается это интересно'}


class BlogCreateView(CreateView):
    model = Blog
    extra_context = {'title': 'Отлично! ты хочешь поделиться интересной статьей'}
    fields = ('title', 'preview', 'content', 'is_published')
    success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        if form.is_valid:
            new_nat = form.save()
            new_nat.slug = slugify(new_nat.title)
            new_nat.save()
            return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    extra_context = {'title': 'Что случилось? ты хочешь изменить?'}
    fields = ('title', 'preview', 'content', 'is_published')
    # success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        if form.is_valid:
            new_nat = form.save()
            new_nat.slug = slugify(new_nat.title)
            new_nat.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:view_blog', args=[self.kwargs.get("slug")])


class BlogDeleteView(DeleteView):
    model = Blog
    extra_context = {'title': 'Всё  неправда и скучно'}
    success_url = reverse_lazy('catalog:blog')


class BlogDetailView(DetailView):
    model = Blog
    extra_context = {'title': 'Интересно...'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        if self.object.views_count == 100:
            send_mail(
                "Поздравляю",
                f"Количество просмотров достигло 100, блог: '{self.object.title}'.",
                "knopisha.zh@gmail.com",
                ["knopisha.zh@gmail.com"],
                fail_silently=False,
            )
        return self.object

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset
