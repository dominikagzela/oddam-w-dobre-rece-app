from django.db import models
from django.contrib.auth.models import User

INSTITUTION = (
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna'),
)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"


class Institution(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    type = models.PositiveSmallIntegerField(choices=INSTITUTION, default=1)
    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name = "Instytucja"
        verbose_name_plural = "Instytucje"


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.PositiveIntegerField()
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True)
    user = models.ForeignKey(User, null=True, default='', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Darowizna"
        verbose_name_plural = "Darowizny"
