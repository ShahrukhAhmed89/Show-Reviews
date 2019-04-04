from django.db import models
from django.contrib.postgres.fields import ArrayField
from chingu.models import Chingu
from dramas.models import Show


# Create your models here.

class Reviews(models.Model):
	user        		= models.ForeignKey(Chingu, on_delete=models.CASCADE,  related_name="review_author")
	show        		= models.ForeignKey(Show, on_delete=models.CASCADE)
	rating      		= models.DecimalField(default=0, max_digits=3, decimal_places=1)
	post      			= models.TextField()
	has_post 			= models.BooleanField(default=False)
	user_likes  		= ArrayField(models.IntegerField(), blank=True, null=True, default=list)
	user_like_count 	= models.IntegerField(default=0)
	post_date_created	= models.DateField(auto_now=True)
	post_date_edited	= models.DateField(auto_now_add=True)

	class Meta:
		ordering = ['-user_like_count']
		verbose_name_plural = "Reviews"



	def __str__(self):
		return self.show.title + ' review by ' + str(self.user)

