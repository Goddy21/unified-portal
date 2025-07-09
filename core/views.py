from django.shortcuts import render, get_list_or_404, redirect
from .models import File, FileCategory
from django.http import FileResponse
from .forms import FileUploadForm, ProblemCategoryForm, TicketForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.db.models import Count, Q
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
from core.models import FileCategory
import os
from collections import Counter
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from .forms import UserUpdateForm, ProfileUpdateForm, TerminalForm, VersionControlForm, FileUploadForm, CustomUserCreationForm
from django.views import View
import csv
from .models import Customer, Region, Terminal, Unit, SystemUser, Zone, ProblemCategory, VersionControl, Report, Ticket, Profile
from django.contrib import messages
from datetime import datetime
from django.utils.dateparse import parse_date
from django.utils import timezone
import calendar
from django.shortcuts import get_object_or_404
from mimetypes import guess_type
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login
from django import forms

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()
def is_editor(user):
    return user.groups.filter(name='Editor').exists()
def is_viewer(user):
    return user.groups.filter(name='Viewer').exists()
def is_customer(user):
    return user.groups.filter(name='Customer').exists()

@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_files': File.objects.count(),
        'open_tickets': Ticket.objects.filter(status='open').count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('create_user')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        messages.success(request, f"{role} user created successfully.")
        return redirect('admin_dashboard')

    return render(request, 'accounts/create_user.html')

@user_passes_test(is_admin)
def manage_user_roles(request):
    users = User.objects.exclude(username=request.user.username)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('new_role')

        user = get_object_or_404(User, id=user_id)
        user.groups.clear()
        group, _ = Group.objects.get_or_create(name=new_role)
        user.groups.add(group)

        messages.success(request, f"{user.username}'s role updated to {new_role}.")
        return redirect('manage_user_roles')

    return render(request, 'accounts/manage_user_roles.html', {'users': users})

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
@permission_required('core.view_file', raise_exception=True)
def view_files(request):
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})

@login_required
@permission_required('core.change_file', raise_exception=True)
def edit_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, instance=file)
        if form.is_valid():
            form.save()
            return redirect('view_files')
    else:
        form = FileUploadForm(instance=file)

    return render(request, 'edit_file.html', {'form': form, 'file': file})

def pre_dashboards(request):
    return render(request, 'core/pre_dashboards.html')

@user_passes_test(is_viewer)
def user_list_view(request):
    users = User.objects.all()
    return render(request, 'core/file_management/user_list.html', {'users': users})

@user_passes_test(is_viewer)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'core/file_management/user_detail.html', {'user': user})

@user_passes_test(is_editor)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.is_active = 'is_active' in request.POST
        user.save()
        messages.success(request, 'User updated successfully!')
        return redirect('user_list')
    return render(request, 'core/file_management/edit_user.html', {'user': user})

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('user_list')

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


    return render(request, 'core/file_management/dashboard.html', {
        'categories': categories,
        'recent_files': recent_files,
        'file_types': file_types,
        'user_name': request.user.get_full_name() or request.user.username  
    })

#@user_passes_test(is_viewer)
def file_list_view(request, category_name=None):
    files = File.objects.filter(is_deleted=False)

    if category_name:
        files = files.filter(category__name__iexact=category_name)
        
    sort_option = request.GET.get('sort')
    if sort_option == 'recent':
        files = files.order_by('-upload_date')
    else:
        files = files.order_by('title')
         # PAGINATION START
    paginator = Paginator(files, 10) 
    page = request.GET.get('page')
    try:
        paginated_files = paginator.page(page)
    except PageNotAnInteger:
        paginated_files = paginator.page(1)
    except EmptyPage:
        paginated_files = paginator.page(paginator.num_pages)
    # PAGINATION END
    categories = FileCategory.objects.all()  

    return render(request, 'core/file_management/file_list.html', {
        'files': paginated_files,
        'categories': categories,
        'active_category': category_name,
    })

#@user_passes_test(is_viewer)
#@permission_required('core.view_file', raise_exception=True)
def preview_file(request, file_id):
    file = get_object_or_404(File, id=file_id, is_deleted=False)

    # Get the guessed content type (e.g., image/jpeg, application/pdf)
    mime_type, _ = guess_type(file.file.name)
    if mime_type in ['application/pdf', 'image/jpeg', 'image/png', 'image/gif']:
        return FileResponse(file.file.open('rb'), content_type=mime_type)
    
    # If unsupported, render fallback page
    return render(request, 'core/file_management/unsupported_preview.html', {'file': file})

@login_required
@permission_required('core.delete_file', raise_exception=True)
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, is_deleted=False)

    if request.method == "POST":
        file.is_deleted = True
        file.save()
        messages.success(request, "File deleted successfully.")
        return redirect('file_list')
    
@login_required
@permission_required('core.add_file', raise_exception=True)
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

@user_passes_test(is_viewer)
def profile_view(request):
    context = {
        'user': request.user,
        'user_form': UserUpdateForm(instance=request.user),
        'profile_form': ProfileUpdateForm(instance=request.user.profile),
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'accounts/profile_content.html', context)

    return render(request, 'accounts/profile.html', context)


@method_decorator(login_required, name='dispatch')
class SettingsView(View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        return render(request, 'accounts/settings.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_view')
        return render(request, 'accounts/settings.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })


# Tickets
def ticketing_dashboard(request):
    # Status summary
    status_counts = Ticket.objects.values('status').annotate(count=Count('id'))

    # Priority summary
    priority_counts = Ticket.objects.values('priority').annotate(count=Count('id'))

    # Monthly ticket trends
    monthly_trends = (
        Ticket.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Tickets per terminal
    terminal_data = (
        Ticket.objects
        .values('terminal__cdm_name')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    context = {
        'status_data': list(status_counts),
        'priority_data': list(priority_counts),
        'monthly_data': [
            {'month': calendar.month_abbr[d['month'].month], 'count': d['count']}
            for d in monthly_trends if d['month']  # Guard against None
        ],
        'terminal_data': [
            {'terminal': d['terminal__cdm_name'], 'count': d['count']}
            for d in terminal_data
        ],
    }

    return render(request, 'core/helpdesk/ticketing_dashboard.html', context)

def tickets(request):
    query = request.GET.get('search', '')
    tickets = Ticket.objects.select_related('problem_category').filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(problem_category__name__icontains=query)
    ).order_by('-created_at')

    return render(request, 'core/helpdesk/tickets.html', {
        'tickets': tickets,
        'search_query': query
    })


def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('create_ticket' if 'create_another' in request.POST else 'ticketing_dashboard')
    else:
        form = TicketForm()

    return render(request, 'core/helpdesk/create_ticket.html', {'form': form})

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'core/helpdesk/ticket_detail.html', {'ticket': ticket})

@user_passes_test(is_admin)
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()
    messages.success(request, "Ticket deleted successfully.")
    return redirect('tickets')

def ticket_statuses(request):
    return render(request, 'core/helpdesk/ticket_statuses.html')

def problem_category(request):
    query = request.GET.get('search', '')
    categories = ProblemCategory.objects.filter(name__icontains=query)
    return render(request, 'core/helpdesk/problem_category.html', {
        'categories': categories,
        'search_query': query,
    })

@user_passes_test(is_admin)
def create_problem_category(request):
    if request.method == 'POST':
        form = ProblemCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()

            if 'create_another' in request.POST:
                return redirect('create_problem_category')
            return redirect('problem_category')  
    else:
        form = ProblemCategoryForm()

    return render(request, 'core/helpdesk/create_problem_category.html', {'form': form})

@user_passes_test(is_admin)
def edit_problem_category(request, category_id):
    category = get_object_or_404(ProblemCategory, pk=category_id)
    if request.method == 'POST':
        form = ProblemCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('problem_category')
    else:
        form = ProblemCategoryForm(instance=category)

    return render(request, 'core/helpdesk/edit_problem_category.html', {'form': form})

@user_passes_test(is_admin)
def delete_problem_category(request, category_id):
    category = get_object_or_404(ProblemCategory, id=category_id)
    category.delete()
    messages.success(request, "Problem category deleted successfully.")
    return redirect('problem_category')


def list_problem_categories(request):
    categories = ProblemCategory.objects.all()
    return render(request, 'core/helpdesk/problem_category.html', {'categories': categories})

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

@user_passes_test(is_admin)
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

@user_passes_test(is_admin)
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    messages.success(request, "Customer deleted successfully.")
    return redirect('customers')

def regions(request):
    if request.method == 'POST':
        name = request.POST.get('region_name')
        if name:
            Region.objects.create(name=name)
            return redirect('regions')

    all_regions = Region.objects.all()
    return render(request, 'core/helpdesk/regions.html', {'regions': all_regions})

@user_passes_test(is_admin)
def delete_region(request, region_id):
    region = get_object_or_404(Region, id=region_id)
    region.delete()
    messages.success(request, "Region deleted successfully.")
    return redirect('regions')

def terminals(request):
    if request.method == 'POST':
        form = TerminalForm(request.POST)
        if form.is_valid():
            form.save()
            if 'create_another' in request.POST:
                return redirect('terminals')
            else:
                return redirect('terminals') 
    else:
        form = TerminalForm()

    all_terminals = Terminal.objects.all()
    return render(request, 'core/helpdesk/terminals.html', {'form': form, 'terminals': all_terminals})

@user_passes_test(is_admin)
def delete_terminal(request, terminal_id):
    terminal = get_object_or_404(Terminal, id=terminal_id)
    terminal.delete()
    messages.success(request, "Terminal removed successfully.")
    return redirect('terminals')

def units(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            Unit.objects.create(name=name, description=description)
        return redirect('units')

    all_units = Unit.objects.all()
    return render(request, 'core/helpdesk/units.html', {'units': all_units})

@user_passes_test(is_admin)
def delete_unit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    unit.delete()
    messages.success(request, "Unit removed successfully.")
    return redirect('units')

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

@user_passes_test(is_admin)
def delete_system_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user == user:
        messages.error(request, "You cannot delete your own account.")
    else:
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect('system_users')

def zones(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        region_id = request.POST.get('region')

        if name and region_id:
            region = get_object_or_404(Region, pk=region_id)
            Zone.objects.create(name=name, region=region)
            messages.success(request, "Zone created successfully.")
            return redirect('zones')
        else:
            messages.error(request, "Name and region are required.")

    all_zones = Zone.objects.all()
    all_regions = Region.objects.all()  

    return render(request, 'core/helpdesk/zones.html', {
        'zones': all_zones,
        'regions': all_regions
    })

@user_passes_test(is_admin)
def delete_zone(request, zone_id):
    zone = get_object_or_404(Zone, id=zone_id)
    zone.delete()
    messages.success(request, "Zone deleted successfully.")
    return redirect('zones') 

def reports(request):
    reports_qs = Report.objects.all()

    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category:
        reports_qs = reports_qs.filter(category=category)

    if start_date:
        reports_qs = reports_qs.filter(generated_at__date__gte=parse_date(start_date))
    if end_date:
        reports_qs = reports_qs.filter(generated_at__date__lte=parse_date(end_date))

    return render(request, 'core/helpdesk/reports.html', {
        'reports': reports_qs
    })


def version_controls(request):
    if request.method == 'POST':
        form = VersionControlForm(request.POST)
        if form.is_valid():
            form.save()
            if 'create_another' in request.POST:
                return redirect('version_controls')
            else:
                return redirect('version_controls')
    else:
        form = VersionControlForm()

    versions = VersionControl.objects.all().order_by('-created_at')

    return render(request, 'core/helpdesk/version_control.html', {
        'form': form,
        'versions': versions
    })