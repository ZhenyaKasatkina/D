import secrets

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.func import make_random_password

from users.models import User


class RegisterView(CreateView):
    """
    Регистрация нового пользователя
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Отправка пользователю ссылки для проверки подлинности данных
        """
        user = form.save()
        # print(user)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        # print(url)
        send_mail(
            subject='подтверждение почты на нашем сайте',
            message=f'Привет!\n Прейдите по ссылке в подтверждение своей почты \n '
                    f'{url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    """
    Проверка подлинности ч/з ссылку
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def password_recovery(request):
    """
    Восстановление пароля
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        # print(f"есть {email}")      # проверка наличия адреса в БД

        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            # characters = string.ascii_letters + string.digits + string.punctuation
            # new_password = ''.join(secrets.choice(characters) for item in range(10))
            new_password = make_random_password()
            user.password = make_password(password=new_password, salt=None, hasher='default')
            # user.set_password(new_password)
            user.save()
            # print(user.password)
            send_mail(
                subject='Восстановление пароля',
                message=f'Привет! новый пароль для входа на сайт: \n'
                        f'{new_password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            return HttpResponseRedirect(reverse_lazy('users:login'))

        else:
            print('нет в БД')
            return HttpResponseRedirect(reverse_lazy('users:login'))

    return render(request, 'users/password_recovery.html')


class ProfileView(UpdateView):
    """
    Данные активного пользователя и возможность их изменения
    """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('catalog:homepage')

    def get_object(self, queryset=None):
        return self.request.user
