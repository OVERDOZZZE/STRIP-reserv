from django.db import models

from user.models import CustomUser


# Create your models here.


class Tour(models.Model):
    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

    COMPLEXITY_CHOICES = (
        ('e', 'Легкий'),
        ('m', 'Средний'),
        ('h', 'Сложный'),
        ('s-h', 'Экстра-сложный')
    )
    DURATION_CHOICES = (
        ('1', 'День'),
        ('3', 'Три дня'),
        ('7', 'Неделя'),
    )
    title = models.CharField(max_length=255, verbose_name='Название тура')
    description = models.TextField(verbose_name='Описание тура')
    price = models.FloatField('Цена')
    image = models.ImageField(blank=True, null=True, verbose_name='Изображения')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Категория')
    slug = models.SlugField(unique=True)
    date_published = models.DateField(auto_now=True, verbose_name='Дата публикации')
    date_departure = models.DateTimeField("Дата и время выезда")
    date_arrival = models.DateTimeField("Дата и время приезда")
    from_where = models.ForeignKey('Place', on_delete=models.CASCADE, verbose_name='Откуда', related_name='from_where')
    to = models.ForeignKey('Place', on_delete=models.CASCADE, verbose_name='Куда', related_name="to")
    quantity_limit = models.PositiveIntegerField(null=True)
    actual_limit = models.IntegerField(editable=False, null=True, default=30)
    is_hot = models.BooleanField(null=True, blank=True, verbose_name='Горячий тур')
    # duration = models.ForeignKey('Duration', on_delete=models.CASCADE, null=True, verbose_name='Длительность')
    complexity = models.CharField('Сложность', max_length=255, choices=COMPLEXITY_CHOICES, default='')

    def __str__(self):
        return self.title
    #
    # def get_absolute_url(self):
    #     return reverse('tour_detail', kwargs={'tour_slug': self.slug})
    #
    # @property
    # def get_image(self):
    #     try:
    #         url = self.image.url
    #     except:
    #         url =''
    #     return url


class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    text = models.TextField(verbose_name='Отзыв', help_text='Текст отзыва')
    post = models.ForeignKey(Tour, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Place(models.Model):
    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    name_city = models.CharField(max_length=255)
    name_place = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.name_place:
            return self.name_place
        else:
            return self.name_city