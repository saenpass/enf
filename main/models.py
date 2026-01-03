from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории'
    )
    slug = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Slug'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Размер'
    )

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='product_sizes',
        verbose_name='Товар'
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        verbose_name='Размер'
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество на складе'
    )

    class Meta:
        verbose_name = 'Размер товара'
        verbose_name_plural = 'Размеры товаров'
        unique_together = ('product', 'size')

    def __str__(self):
        return f'{self.product.name} — {self.size.name} (в наличии: {self.stock})'


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название товара'
    )
    slug = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Slug'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    color = models.CharField(
        max_length=100,
        verbose_name='Цвет'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    main_image = models.ImageField(
        upload_to='products/main/',
        verbose_name='Основное изображение'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField(
        upload_to='products/extra/',
        verbose_name='Дополнительное изображение'
    )

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self):
        return f'Изображение для {self.product.name}'
