from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category, Author
from django.utils.translation import gettext as _

class PostForm(forms.ModelForm):
    author_post = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label=_('выберите автора'), label=_('Автор'))
    post_category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label=_('Категория'),)
    title = forms.CharField(max_length=255, label=_('Название'))


    class Meta:
        model = Post
        fields = [
            'author_post',
            'title',
            'text_post',
            'post_category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text_post = cleaned_data.get("text_post")
        title = cleaned_data.get("title")
        if title == text_post:
            raise ValidationError(
                _("Текст публикации не должен быть идентичен названию.")
            )
        return cleaned_data