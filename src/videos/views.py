from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .models import Video
from .forms import VideoUploadForm
from .utils import generate_video_thumbnail
import threading

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videos/video_list.html', {'videos': videos})

def video_upload(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            
            # Generate thumbnail in background to not block response
            # For a production app, use Celery. For this simple local app, threading is okay.
            try:
                t = threading.Thread(target=generate_video_thumbnail, args=(video,))
                t.start()
            except Exception as e:
                print(f"Error starting thumbnail generation thread: {e}")

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'redirect_url': reverse('video_detail', args=[video.pk])
                })
            
            messages.success(request, '影片上傳成功！縮圖正在生成中。')
            return redirect('video_detail', pk=video.pk)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = VideoUploadForm()
    return render(request, 'videos/upload.html', {'form': form})

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, 'videos/video_detail.html', {'video': video})

def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video.delete()
        messages.success(request, '影片已刪除。')
        return redirect('video_list')
    return render(request, 'videos/confirm_delete.html', {'video': video})
