from django.db import models

# Create your models here.
class Post(models.Model):
    post_title = models.CharField(max_length=60)
    post_content = models.TextField()
    pundlished_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.post_title