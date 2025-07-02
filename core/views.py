from django.shortcuts import render, get_list_or_404, redirect
from .models import File, FileCategory
from .forms import FileUploadForm, ProblemCategoryForm, TicketForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from core.models import FileCategory
import os
from collections import Counter
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .forms import UserUpdateForm, ProfileUpdateForm
from django.views import View
import csv
from .models import Customer, Region, Terminal, Unit, SystemUser, Zone
from django.contrib import messages
from datetime import datetime

def login(request):
    return render(request, 'core/login.html')

def pre_dashboards(request):
    return render(request, 'core/pre_dashboards.html')

def user_list_view(request):
    users = User.objects.all()
    return render(request, 'core/file_management/user_list.html', {'users': users})

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


    return render(request, 'core/file_management/file_management_dashboard.html', {
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

    return render(request, 'core/file_management/file_list.html', {
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
    
    return render(request, 'core/file_management/upload_file.html', {'form': form})

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
    return render(request, 'core/helpdesk/admin_dashboard.html')

def ticketing_dashboard(request):
    return render(request, 'core/helpdesk/ticketing_dashboard.html')

def tickets(request):
    return render(request, 'core/helpdesk/tickets.html')

def create_ticket(request):
    if request.method == 'POST':
        form  = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('ticketing_dashboard') 
    else:
        form = TicketForm()

    return render(request, 'core/helpdesk/create_ticket.html', {'form': form})   


def ticket_statuses(request):
    return render(request, 'core/helpdesk/ticket_statuses.html')

def problem_category(request):
    return render(request, 'core/helpdesk/problem_category.html')

def create_problem_category(request):
    if request.method == 'POST':
        form = ProblemCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if 'create_another' in request.POST:
                return redirect('create-problem-category')
            return redirect('category-list')  # Or wherever you want to go after creation
    else:
        form = ProblemCategoryForm()

    return render(request, 'core/helpdesk/create_problem_category.html', {'form': form})

# Master Data Views
def customers(request):
    if request.method == "POST" and request.FILES.get("file"):
        csv_file = request.FILES["file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            name = row.get("name", "").strip()
            if name: 
                Customer.objects.create(name=name)

        messages.success(request, "Customers uploaded successfully!")


    all_customers = Customer.objects.exclude(name__exact="").exclude(name__isnull=True)
    return render(request, "core/helpdesk/customers.html", {"customers": all_customers})


def create_customer(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            Customer.objects.create(name=name)
            messages.success(request, "Customer added successfully.")
            return redirect("customers")
        else:
            messages.error(request, "Customer name is required.")

    return render(request, "core/helpdesk/create_customer.html")

def regions(request):
    if request.method == 'POST':
        name = request.POST.get('region_name')
        if name:
            Region.objects.create(name=name)
            return redirect('regions')

    all_regions = Region.objects.all()
    return render(request, 'core/helpdesk/regions.html', {'regions': all_regions})

def terminals(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        if name and location:
            Terminal.objects.create(name=name, location=location)
        return redirect('terminals')

    all_terminals = Terminal.objects.all()
    return render(request, 'core/helpdesk/terminals.html', {'terminals': all_terminals})

def units(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            Unit.objects.create(name=name, description=description)
        return redirect('units')

    all_units = Unit.objects.all()
    return render(request, 'core/helpdesk/units.html', {'units': all_units})

def system_users(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        if username and email and role:
            SystemUser.objects.create(username=username, email=email, role=role)
        return redirect('system_users')

    all_users = SystemUser.objects.all()
    return render(request, 'core/helpdesk/users.html', {'users': all_users})

def zones(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        region = request.POST.get('region')
        if name and region:
            Zone.objects.create(name=name, region=region)
        return redirect('zones')

    all_zones = Zone.objects.all()
    return render(request, 'core/helpdesk/zones.html', {'zones': all_zones})

# Reports Views
def reports(request):
    # Sample dummy data — you can replace with DB results
    reports_data = [
        {"name": "Ticket Summary", "category": "tickets", "generated_at": "2025-06-25", "download_url": "#"},
        {"name": "User Activity", "category": "users", "generated_at": "2025-06-24", "download_url": "#"},
    ]

    return render(request, 'core/helpdesk/reports.html', {
        'reports': reports_data
    })

version_data = []

def version_controls(request):
    global version_data

    if request.method == 'POST':
        version = request.POST.get('version')
        description = request.POST.get('description')
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        version_data.insert(0, {
            'version': version,
            'description': description,
            'date': date,
        })
        return redirect('version_controls')

    return render(request, 'core/helpdesk/version_control.html', {
        'versions': version_data
    })
