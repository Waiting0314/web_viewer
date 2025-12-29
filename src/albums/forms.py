from django import forms
from .models import Album, Tag

class TagFieldMixin:
    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        if not tags_str:
            return []
        return [t.strip() for t in tags_str.split(',') if t.strip()]

    def save_tags(self, album):
        tag_names = self.cleaned_data.get('tags', [])
        album.tags.clear()
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            album.tags.add(tag)

class AlbumUploadForm(forms.ModelForm, TagFieldMixin):
    zip_file = forms.FileField(
        label='相片壓縮檔 (Zip)',
        help_text='請上傳包含照片的 .zip 檔案',
        widget=forms.FileInput(attrs={'accept': '.zip'}),
        required=False # Make it optional to allow folder upload later, or handle validation
    )
    tags = forms.CharField(
        label='標籤',
        required=False,
        help_text='請輸入標籤，以逗號分隔 (例如: 風景, 旅遊)',
        widget=forms.TextInput(attrs={'placeholder': '風景, 旅遊'})
    )

    class Meta:
        model = Album
        fields = ['title', 'description', 'cover_image']
        labels = {
            'title': '相簿標題',
            'description': '描述',
            'cover_image': '封面圖片 (選填)',
        }

    def save(self, commit=True):
        album = super().save(commit=False)
        if commit:
            album.save()
            self.save_tags(album)
        return album

class AlbumEditForm(forms.ModelForm, TagFieldMixin):
    tags = forms.CharField(
        label='標籤',
        required=False,
        help_text='請輸入標籤，以逗號分隔',
    )

    class Meta:
        model = Album
        fields = ['title', 'description', 'cover_image']
        labels = {
            'title': '相簿標題',
            'description': '描述',
            'cover_image': '封面圖片 (選填)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join([t.name for t in self.instance.tags.all()])

    def save(self, commit=True):
        album = super().save(commit=False)
        if commit:
            album.save()
            self.save_tags(album)
        return album
