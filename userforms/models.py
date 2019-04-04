from django.db import models

# Create your models here

class Feedback(models.Model):
    choices = (
        ('Can you add this show', 'Can you add this show'),
        ('Can you add this feature', 'Can you add this feature'),
        ('There is a problem with the website', 'There is a problem with the website'),
        ('Other Feedback', 'Other Feedback'),
    )
    problem = models.CharField(max_length=50, choices=choices, default = 'Can you add this show')
    text    = models.TextField()
    

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"

    def __str__(self):
        return self.problem

    def get_absolute_url(self):
        return reverse("feedback", kwargs={"pk": self.pk})
