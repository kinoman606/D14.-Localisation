from django.core.management import BaseCommand, CommandError
from django.utils.translation import gettext as _
from news.models import Post, Category


class Command(BaseCommand):
    help = _('Удаляет публикации определенной категории')
    missing_args_message = _('Категория удаляемых сообщений указана не корректно')

    def add_arguments(self, parser):
        parser.add_argument("category", type=str)

    def handle(self, *args, **options):
        message = input(f'{_("Вы хотите удалить все сообщения в категории")} {options["category"]}? yes/no:  ')

        if message == 'yes':
            try:
                category = Category.objects.get(name_cat=options['category'])
                posts = Post.objects.filter(post_category=category)
                posts.delete()
                self.stdout.write(self.style.SUCCESS(f'{_("Все публикации из категории")} {category.name_cat} {_("успешно удалены!")}'))
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'{_("Категория")} {category.name_cat} {_("не найдена")}'))
        else:
            self.stdout.write(self.style.ERROR(_('Удаление отменено!')))

            


