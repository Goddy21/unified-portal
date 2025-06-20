from django.shortcuts import render, get_list_or_404, redirect
from .models import File, FileCategory
from .forms import FileUploadForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from core.models import FileCategory
import os
from collections import Counter
from django.contrib.auth.models import User


def login(request):
    return render(request, 'core/login.html')

def pre_dashboards(request):
    return render(request, 'core/pre_dashboards.html')

def user_list_view(request):
    users = User.objects.all()
    return render(request, 'core/user_list.html', {'users': users})

def file_management_dashboard(request):
    files = File.objects.filter(is_deleted=False)
    
    ext_counter = Counter()
    for f in files:
        ext = os.path.splitext(f.file.name)[1].lower()
        ext_counter[ext] += 1

    file_types = [
        {"type": "PDF Documents", "ext": ".pdf", "icon": "fas fa-file-pdf", "count": ext_counter[".pdf"]},
        {"type": "Word Documents", "ext": ".docx", "icon": "fas fa-file-word", "count": ext_counter[".docx"]},
        {"type": "Images", "ext": ".jpg", "icon": "fas fa-file-image", "count": ext_counter[".jpg"] + ext_counter[".png"]},
        {"type": "Excel Sheets", "ext": ".xlsx", "icon": "fas fa-file-excel", "count": ext_counter[".xlsx"]},
        {"type": "Others", "ext": "other", "icon": "fas fa-file", "count": sum(ext_counter.values()) - (
            ext_counter[".pdf"] + ext_counter[".docx"] + ext_counter[".jpg"] + ext_counter[".png"] + ext_counter[".xlsx"]
        )},
    ]

    categories = FileCategory.objects.annotate(
        file_count=Count('file', filter=Q(file__is_deleted=False))
    )

    recent_files = File.objects.filter(is_deleted=False).order_by('-upload_date')[:5]


    return render(request, 'core/file_management_dashboard.html', {
        'categories': categories,
        'recent_files': recent_files,
        'file_types': file_types,
        'user_name': request.user.get_full_name() or request.user.username  
    })


def file_list_view(request, category_name=None):
    files = File.objects.filter(is_deleted=False)

    if category_name:
        files = files.filter(category__name__iexact=category_name)
        
    sort_option = request.GET.get('sort')
    if sort_option == 'recent':
        files = files.order_by('-upload_date')
    else:
        files = files.order_by('title')
    categories = FileCategory.objects.all()  

    return render(request, 'core/file_list.html', {
        'files': files,
        'categories': categories,
        'active_category': category_name,
    })

@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.uploaded_by = request.user
            file_instance.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    
    return render(request, 'core/upload_file.html', {'form': form})

def ticketing_dashboard(requrest):
    return render(requrest, 'core/ticketing_dashboard.html')