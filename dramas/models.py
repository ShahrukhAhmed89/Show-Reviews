from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.urls import reverse


# Create your models here.
class Show(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField(auto_now=False, auto_now_add=False)
    synopsis = models.TextField(null=True, blank=True)
    image_portrait = models.ImageField(null=True, upload_to="show/")
    image_landscape = models.ImageField(null=True, upload_to="show/")
    tmdb_data = JSONField(null=True, blank=True)
    meta_data = JSONField(null=True, blank=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("show:show_page", kwargs={"id":self.id, "slug":self.slug})
