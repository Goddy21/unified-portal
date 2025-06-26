from django.shortcuts import render, get_list_or_404, redirect
from .models import File, FileCategory
from .forms import FileUploadForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from core.models import FileCategory
import os
from collections import Counter
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .forms import UserUpdateForm, ProfileUpdateForm
from django.views import View


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
        {"type": "PDF Documents", "ext": ".pdf", "icon": "fas fa-file-pdf", "count": ext_counter.get(".pdf", 0)},
        {"type": "Word Documents", "ext": ".docx", "icon": "fas fa-file-word", "count": ext_counter.get(".docx", 0)},
        {"type": "Images", "ext": ".jpg", "icon": "fas fa-file-image", "count": ext_counter.get(".jpg", 0) + ext_counter.get(".png", 0)},
        {"type": "Excel Sheets", "ext": ".xlsx", "icon": "fas fa-file-excel", "count": ext_counter.get(".xlsx", 0)},
        {"type": "Others", "ext": "other", "icon": "fas fa-file", "count": sum(ext_counter.values()) - (
            ext_counter.get(".pdf", 0) + ext_counter.get(".docx", 0) + ext_counter.get(".jpg", 0) +
            ext_counter.get(".png", 0) + ext_counter.get(".xlsx", 0)
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

@login_required
def profile_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'accounts/profile_content.html', {'user': request.user})
    return render(request, 'accounts/profile.html', {'user': request.user})



@method_decorator(login_required, name='dispatch')
class SettingsView(View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'accounts/settings.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_view')
        return render(request, 'accounts/settings.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

# Tickets
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')

def ticketing_dashboard(request):
    return render(request, 'core/ticketing_dashboard.html')

def tickets(request):
    return render(request, 'core/tickets.html')

def ticket_statuses(request):
    return render(request, 'core/ticket_statuses.html')

def problem_category(request):
    return render(request, 'core/problem_category.html')

# Master Data Views
def customers(request):
    return render(request, 'core/customers.html')

def regions(request):
    return render(request, 'core/regions.html')

def terminals(request):
    return render(request, 'core/terminals.html')

def units(request):
    return render(request, 'core/units.html')

def system_users(request):  
    return render(request, 'core/users.html')

def zones(request):
    return render(request, 'core/zones.html')

# Reports Views
def reports(request):
    return render(request, 'core/reports.html')

def version_controls(request):
    return render(request, 'core/version_control.html')
