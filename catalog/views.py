from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.forms import inlineformset_factory
# from django.shortcuts import render   # ДЗ 20.1
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm, VersionFormSet, ProductModeratorForm
# from catalog.management.commands.fill import Command   #ДЗ 20.1
from catalog.models import MyContact, Product, Category, UserContacts, Blog, Version
from catalog.services import get_category_from_cache
from config.settings import EMAIL_HOST_USER


class CategoryListView(ListView):
    model = Category
    extra_context = {'title': 'Страница категорий Вкусняшек'}

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     get_category_from_cache()
    #     return context_data

    def get_queryset(self):
        return get_category_from_cache()


class ProductListView(ListView):
    model = Product
    extra_context = {'title': 'Главная страница Вкусняшек'}
    paginate_by = 5
    orphans = 4

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['category_list'] = Category.objects.all()
        vers = Version.objects.filter(is_active=True)
        context_data['active_versions'] = vers
        user = self.request.user
        context_data['user'] = user
        # print(context_data)
        return context_data

    def get_queryset(self):
        return Product.objects.all().order_by('product_name')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:homepage')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm,
                                               extra=1)
        if self.request.method == 'POST':
            context_data["formset"] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            user = self.request.user
            self.object.owner = user
            self.object.save()
            # print(self.object)
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

#     # five_latest_products = Command.json_read_products()[-5:]  #ДЗ 20.1
#     # for prod in five_latest_products:
#     #     print(prod["fields"]["product_name"])


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    # form_class = ProductForm
    success_url = reverse_lazy('catalog:homepage')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm,
                                               formset=VersionFormSet, extra=1)
        if self.request.method == 'POST':
            # print(f'1 ............. {context_data}, {self.request.method}')
            context_data["formset"] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
            # print(context_data["formset"])
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        """Права доступа владельца, менеджера"""
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if (user.has_perm("catalog.cancel_published_status")
                and user.has_perm("catalog.can_edit_description")
                and user.has_perm("catalog.can_edit_category")):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    extra_context = {
        'title': 'Вот что ты выбрал',
    }


class UserContactsCreateView(CreateView):
    model = UserContacts
    extra_context = {'title': 'Вкусняшка от пользователя'}
    fields = ('name', 'phone', 'email', 'message')
    success_url = reverse_lazy('catalog:homepage')
    print(UserContacts)


class MyContactListView(ListView):
    model = MyContact
    extra_context = {'title': 'Наши Контакты'}


class BlogListView(ListView):
    model = Blog
    extra_context = {'title': '???  Оказывается это интересно'}


class BlogCreateView(PermissionRequiredMixin, CreateView):
    model = Blog
    permission_required = 'catalog.add_blog'
    extra_context = {'title': 'Отлично! ты хочешь поделиться интересной статьей'}
    fields = ('title', 'preview', 'content', 'is_published')
    success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        if form.is_valid:
            new_nat = form.save()
            new_nat.slug = slugify(new_nat.title)
            new_nat.save()
            return super().form_valid(form)


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Blog
    permission_required = 'catalog.change_blog'
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
        return reverse('catalog:blog')


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    permission_required = 'catalog.delete_blog'
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
                EMAIL_HOST_USER,
                ["knopisha.zh@gmail.com"],
                fail_silently=False,
            )
        return self.object

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset
