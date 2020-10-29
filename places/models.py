from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    is_world_herritage = models.BooleanField(default=False)
    is_city_area = models.BooleanField()
    description = models.TextField()
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name
