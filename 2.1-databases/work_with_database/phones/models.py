from django.db import models
from django.urls import reverse


class Phone(models.Model):
    name = models.TextField(max_length=30)
    slug = models.SlugField(null=True)

    price = models.IntegerField()
    image = models.ImageField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.name})

