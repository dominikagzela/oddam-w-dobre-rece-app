from django.db import models

INSTITUTION = (
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna'),
)


class Category(models.Model):
    name = models.CharField(max_length=50)


class Institution(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    type = models.PositiveSmallIntegerField(choices=INSTITUTION, default=1)
    categories = models.ManyToManyField(Category)

