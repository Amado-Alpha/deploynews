from django.db import models

# Create your models here.

class Headline(models.Model):
  title = models.CharField(max_length=200)
  image = models.URLField(null=True, blank=True)
  url = models.TextField()
  notification_sent = models.BooleanField(default=False)
  category = models.CharField(max_length=50, default='General')

  def __str__(self):
    return f"Title: {self.title}, Category: {self.category}"

