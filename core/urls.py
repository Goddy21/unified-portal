from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import SettingsView


urlpatterns = [
    #path('', views.login, name='login'),
    path('', views.pre_dashboards, name='pre_dashboards'),
    path('users/', views.user_list_view, name='user_list'),


    path('files-management/', views.file_management_dashboard, name='file_management_dashboard'),
    path('profile/', views.profile_view, name='profile_view'),
    path('settings/', SettingsView.as_view(), name='settings'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('files/', views.file_list_view, name='file_list'),
    path('files/category/<str:category_name>/', views.file_list_view, name="file_list_by_category"),
    path('files/upload/', views.upload_file_view, name='upload_file'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('ticketing/', views.ticketing_dashboard, name='ticketing_dashboard'),
    path('tickets/', views.tickets, name='tickets'),
    path('ticket-statuses/', views.ticket_statuses, name='ticket_statuses'),
    path('problem-category/', views.problem_category, name='problem_category'), 

    # Master Data
    path('master-data/customers/', views.customers, name='customers'),
    path('master-data/regions/', views.regions, name='regions'),
    path('master-data/terminals/', views.terminals, name='terminals'),
    path('master-data/units/', views.units, name='units'),
    path('master-data/users/', views.system_users, name='system_users'), 
    path('master-data/zones/', views.zones, name='zones'),

    # Reports
    path('reports/general/', views.reports, name='reports'),
    path('reports/version-controls/', views.version_controls, name='version_controls'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
