from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField(null=False, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.caption}'

class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts/', null=True)
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    content = models.TextField(null=False, validators=[MinLengthValidator(25)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.title}'

class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    content = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')