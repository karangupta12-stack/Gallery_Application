from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Album(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def cover_photo(self):
        """Return the first active photo in this album"""
        return self.photos.filter(is_active=True).first()
    
    def __str__(self):
        return self.title

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    is_active = models.BooleanField(default=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
    
    
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return f"Photo by {self.user.username}"
    

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    
    video_file = models.FileField(upload_to='user_videos/')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return f"Video by {self.user.username}"
