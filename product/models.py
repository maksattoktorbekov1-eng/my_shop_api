from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    def _str_(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def _str_(self):
        return self.title

class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def _str_(self):
        return self.text