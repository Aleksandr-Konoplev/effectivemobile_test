from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название продукта')
    description = models.TextField(verbose_name='Описание продукта')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
