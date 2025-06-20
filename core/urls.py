from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.login, name='login'),
    path('', views.pre_dashboards, name='pre_dashboards'),
    path('users/', views.user_list_view, name='user_list'),


    path('files-management/', views.file_management_dashboard, name='file_management_dashboard'),
    path('files/', views.file_list_view, name='file_list'),
    path('files/category/<str:category_name>/', views.file_list_view, name="file_list_by_category"),
    path('files/upload/', views.upload_file_view, name='upload_file'),
    path('ticketing/', views.ticketing_dashboard, name='ticketing_dashboard'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
