from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField('название', max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    name = models.CharField('название', max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class NewsLinks(models.Model):

    class Meta:
        verbose_name = 'ссылка новостей'
        verbose_name_plural = 'ссылки новостей'

    whatsapp = models.URLField(verbose_name='whatsapp', blank=True, null=True)
    telegram = models.URLField(verbose_name='telegram', blank=True, null=True)
    instagram = models.URLField(verbose_name='instagram', blank=True, null=True)
    facebook = models.URLField(verbose_name='facebook', blank=True, null=True)

    news = models.OneToOneField('main.News', on_delete=models.CASCADE, verbose_name='новость', related_name='link')

    def __str__(self):
        return f'{self.news.title}'


class News(models.Model):

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    title = models.CharField(verbose_name='заголовок', max_length=100)
    image = models.ImageField(verbose_name='изображение', upload_to='news_images/', null=True, blank=True)
    category = models.ForeignKey('main.Category',
                                 on_delete=models.PROTECT, verbose_name='категория', related_name='news', null=True)
    tags = models.ManyToManyField('main.Tag', verbose_name='теги', related_name='news')
    content = models.TextField(verbose_name='контент')
    date = models.DateTimeField(verbose_name='дата добавления', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='дата обновления', auto_now=True)
    author = models.CharField(verbose_name='автор')

    def __str__(self):
        return f'{self.title}'

# Create your models here.
