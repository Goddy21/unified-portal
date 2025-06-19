from django.shortcuts import render, get_list_or_404
from .models import File, FileCategory

def login(request):
    return render(request, 'core/login.html')

def pre_dashboards(request):
    return render(request, 'core/pre_dashboards.html')

def file_management_dashboard(request):
    return render(request, 'core/file_management_dashboard.html')

def file_list_view(request, category_name=None):
    files = File.objects.filter(is_deleted=False)

    if category_name:
        files = files.filter(category__name__iexact=category_name)
        
    categories = FileCategory.objects.all()  

    return render(request, 'core/file_list.html', {
        'files': files,
        'categories': categories,
        'active_category': category_name,
    })


def ticketing_dashboard(requrest):
    return render(requrest, 'core/ticketing_dashboard.html')