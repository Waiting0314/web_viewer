from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from .models import Album, Tag
from .forms import AlbumUploadForm, AlbumEditForm
from .utils import handle_zip_upload, handle_folder_upload

def album_list(request):
    albums = Album.objects.all()
    tags = Tag.objects.all()

    # Search
    query = request.GET.get('q')
    if query:
        albums = albums.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )

    # Tag Filter
    tag_filter = request.GET.get('tag')
    if tag_filter:
        albums = albums.filter(tags__name=tag_filter)

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['created_at', '-created_at', 'title', '-title']:
        albums = albums.order_by(sort_by)

    context = {
        'albums': albums,
        'tags': tags,
        'current_tag': tag_filter,
        'current_query': query,
        'current_sort': sort_by,
    }
    return render(request, 'albums/album_list.html', context)

def album_upload(request):
    if request.method == 'POST':
        form = AlbumUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if we have files
            zip_file = form.cleaned_data.get('zip_file')
            folder_files = request.FILES.getlist('folder_files')
            
            if not zip_file and not folder_files:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': '請上傳 Zip 檔案或選擇資料夾'}, status=400)
                messages.error(request, '請上傳 Zip 檔案或選擇資料夾')
                return render(request, 'albums/upload.html', {'form': form})

            album = form.save()
            
            try:
                if zip_file:
                    handle_zip_upload(zip_file, album)
                elif folder_files:
                    handle_folder_upload(folder_files, album)
                
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'redirect_url': reverse('album_detail', args=[album.pk])
                    })
                    
                messages.success(request, f'相簿 "{album.title}" 建立成功！')
                return redirect('album_detail', pk=album.pk)
            except Exception as e:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': f'處理檔案時發生錯誤: {str(e)}'}, status=400)
                messages.error(request, f'處理檔案時發生錯誤: {str(e)}')
                # Optional: album.delete()
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = AlbumUploadForm()
    return render(request, 'albums/upload.html', {'form': form})

def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    photos = album.photos.all()
    
    # Determine view mode from query param, default to 'scroll'
    mode = request.GET.get('mode', 'scroll')
    is_flip_mode = mode == 'flip'
    is_scroll_mode = not is_flip_mode
    
    context = {
        'album': album,
        'photos': photos,
        'mode': mode,
        'is_flip_mode': is_flip_mode,
        'is_scroll_mode': is_scroll_mode,
    }
    return render(request, 'albums/viewer.html', context)

def album_edit(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        form = AlbumEditForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, '相簿更新成功！')
            return redirect('album_detail', pk=album.pk)
    else:
        form = AlbumEditForm(instance=album)
    return render(request, 'albums/edit.html', {'form': form, 'album': album})

def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        album.delete()
        messages.success(request, '相簿已刪除。')
        return redirect('album_list')
    return render(request, 'albums/confirm_delete.html', {'album': album})
