from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your models here.
class Snack(models.Model):
    name = models.CharField(max_length=64)
    purchaser = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('snack_detail', args=[self.id])

    class Meta:
        verbose_name = "Snack"
        verbose_name_plural = "The Snacks"


