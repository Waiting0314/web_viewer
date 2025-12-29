from django.contrib import admin
from .models import Album, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'photo_count')
    inlines = [PhotoInline]

    def photo_count(self, obj):
        return obj.photos.count()

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('filename', 'album', 'order')
    list_filter = ('album',)
