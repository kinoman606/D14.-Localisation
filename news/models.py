from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext as _

class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        post_rat = self.post_set.aggregate(rating_post=Sum('rating'))
        p_rat = 0
        p_rat += post_rat.get('rating_post')

        comment_rat = self.author_user.comment_set.aggregate(rating_comment=Sum('rating'))
        c_rat = 0
        c_rat += comment_rat.get('rating_comment')

        self.rating_author = p_rat * 3 + c_rat
        self.save()

    def __str__(self):
        return f'{self.author_user}'


class Category(models.Model):
    name_cat = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name_cat


class Post(models.Model):
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, _('Новость')),
        (ARTICLE, _('Статья'))
    )
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    date_post = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128, default=_('Новая публикация'))
    text_post = models.TextField()
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text_post[0:123]}...'

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, related_name='subscribers')
    subscription = models.ForeignKey(to='Category', on_delete=models.CASCADE, blank=True, null=True, related_name='subscriptions')



