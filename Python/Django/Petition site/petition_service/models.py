from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField("Категорія", max_length=100)
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Status(models.Model):
    value = models.CharField("Значення", max_length=100)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статуси"

class Petition(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категорія", on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    title = models.CharField("Назва", max_length=100)
    text = models.TextField("Зміст")
    creation_date = models.DateField("Дата створення", default=timezone.now().date())
    status = models.ForeignKey(Status, verbose_name="Статус", on_delete=models.SET_NULL, null=True)
    deleted = models.BooleanField('Видалена', default=False)
    overdue = models.BooleanField('Прострочена', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('petition_detail', kwargs={'id': self.id})

    class Meta:
        verbose_name = "Петиція"
        verbose_name_plural = "Петиції"


class Signature(models.Model):
    signer = models.ForeignKey(User, verbose_name="Користувач", on_delete=models.CASCADE, null=True)
    petition = models.ForeignKey(Petition, verbose_name="Петиція", on_delete=models.CASCADE)

    def __str__(self):
        return self.petition.title + " : " + self.signer.username

    class Meta:
        verbose_name = "Підпис"
        verbose_name_plural = "Підписи"
