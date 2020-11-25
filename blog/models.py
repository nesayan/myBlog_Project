from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BLOG(models.Model):
    title = models.CharField(max_length= 100)
    description = models.TextField(blank= True)
    dateCreated = models.DateTimeField(auto_now_add= True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.title


class COMMENT(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(BLOG, on_delete= models.CASCADE)
    description = models.TextField()
    parent = models.ForeignKey('self', blank= True, null= True, on_delete= models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return "Comment: " + self.description[:20] + " - " + self.user.username