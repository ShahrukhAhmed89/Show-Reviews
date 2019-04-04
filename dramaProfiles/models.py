from django.db import models

# Create your models here.
class Person(models.Model):
    name                = models.CharField( max_length=50 )
    avatar              = models.ImageField(upload_to="person/", null=True, blank=True)
    date_of_birth       = models.DateField( auto_now=False, auto_now_add=False)
    role_choices        =   (
                                ('actor', 'Actor'),
                                ('director', 'Director'),
                                ('writer', 'Writer'),
                                ('actor/director','Actor/Director')
                            )
    role                = models.CharField(max_length=50, choices=role_choices)
    website             = models.URLField(max_length=200, null=True, blank=True)
    facebook_profile    = models.URLField(max_length=200, null=True, blank=True)
    instagram_profile   = models.URLField(max_length=200, null=True, blank=True)
    twitter_profile     = models.URLField(max_length=200, null=True, blank=True)
    v_live              = models.URLField(max_length=200, null=True, blank=True)
    slug                = models.SlugField(max_length=50)

    def __str__(self):
        return self.name