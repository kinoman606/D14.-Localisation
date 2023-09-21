from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *


class CategoryAdmin(TranslationAdmin):
    model = Category


class MyModelAdmin(TranslationAdmin):
    model = Post

@admin.display(description="category")
def category_disp(obj):
    return PostCategory.objects.get(post_through=obj.pk).category_through


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_post', category_disp, 'category_type', 'date_post']
    list_filter = ('author_post', 'date_post')
    search_fields = ['title', 'date_post']


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Subscriber)





