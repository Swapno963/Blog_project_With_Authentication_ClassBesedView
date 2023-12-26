from django.db import models

from categories.models import Category
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.ManyToManyField(Category)
    #akta post multiple categori ar moddha thakte pare abr akta category multiple post thakte pare
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # author ar account delete kora hola tar post gula automatic delete hoea jabe

    # globally image rakbe
    # image = models.ImageField(upload_to='uploads/',blank = True, null = True)

    # app ar moddha rakhbe
    image = models.ImageField(upload_to='posts/media/uploads/',blank = True, null = True)
    def __str__(self) -> str:
        return self.title
    


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)