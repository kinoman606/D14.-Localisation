from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives, mail_managers
from django.utils.translation import gettext as _

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label=_("Имя"))
    last_name = forms.CharField(label=_("Фамилия"))

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        subject = _('Добро пожаловать на Новостной Портал')
        text = f'{user.username}, {_("вы успешно зарегистрировались на сайте")}!'
        html = (f'<b>{user.username}</b>, {_("вы успешно зарегистрировались на")}'
                f'<a href="http://127.0.0.1:8000/news"> {_("сайте")} </a>!')
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()

        mail_managers(
            subject=_('Новый пользователь!'),
            message=f'{_("Пользователь")} {user.username} {_("зарегистрировался на сайте")}.'
        )
        return user



