from django.db import models
import uuid
import os

def album_cover_path(instance, filename):
    return f'albums/{instance.id}/cover_{filename}'

def photo_path(instance, filename):
    return f'albums/{instance.album.id}/photos/{filename}'



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to=album_cover_path, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='albums')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=photo_path)
    order = models.PositiveIntegerField(default=0)
    filename = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.album.title} - {self.filename}"

    class Meta:
        ordering = ['order', 'filename']
