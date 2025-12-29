from django.db import models
import uuid

def video_file_path(instance, filename):
    return f'videos/{instance.id}/{filename}'

def video_cover_path(instance, filename):
    return f'videos/{instance.id}/cover_{filename}'

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=video_file_path)
    cover = models.ImageField(upload_to=video_cover_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
