
from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from .management.commands.runapscheduler import my_job
from .models import Post, Subscriber
from django.utils.translation import gettext as _

@shared_task
def new_post_notify(id):
    new_post = Post.objects.get(id=id)
    categories = new_post.post_category.all()
    emails = []
    for category in categories:
        subs = Subscriber.objects.filter(subscription=category)
        for sub in subs:
            emails.append(sub.user.email)

    subject = f'{_("Новая публикация в категории")} {new_post.post_category}'

    text_content = (
        f'{_("Название публикации")}: {new_post.title}\n'
        f'{_("Автор публикации")}: {new_post.author_post}\n'
        f'{_("Тип публикации")}: {new_post.category_type}\n\n'
        f'{_("Ссылка на публикацию")}: http://127.0.0.1:8000{new_post.get_absolute_url()}'
    )
    html_content = (
        f'{_("Название публикации")}: {new_post.title}<br>'
        f'{_("Автор публикации")}: {new_post.author_post}<br>'
        f'{_("Тип публикации")}: {new_post.category_type}<br><br>'
        f'<a href="http://127.0.0.1:8000{new_post.get_absolute_url()}">{_("Ссылка на публикацию")}</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def sending():
    my_job()

