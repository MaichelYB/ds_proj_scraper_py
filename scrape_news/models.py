from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200)
    highlight = models.TextField()
    content = models.TextField()
    checksum = models.CharField(max_length=128, default="")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
