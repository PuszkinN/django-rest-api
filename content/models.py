from django.db import models
from django.conf import settings


class Movie(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movie_author')
    video = models.FileField(upload_to='content/videos')
    title = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)
    description  = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='movie_likes')
    dis_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='movie_dislikes')
    views = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.title} by {self.author}'

    def comments_count(self):
        return Comment.objects.filter(post=self).count()
    
    def likes_count(self):
        return self.likes.count()
    
    def dislikes_count(self):
        return self.dis_likes.count()



class Photo(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_author', null=True)
    image = models.ImageField(upload_to='content/pictures')
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='photo_likes')
    
    def __str__(self):
        return f'{self.author} - {self.timestamp}'


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_comments', null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_author')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
