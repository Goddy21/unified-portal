from django.urls import path
from . import views

urlpatterns = [
    #path('', views.login, name='login'),
    path('', views.pre_dashboards, name='pre_dashboards'),

    path('files-management/', views.file_management_dashboard, name='file_management_dashboard'),
    path('files/', views.file_list_view, name='file_list'),
    path('files/category/<str:category_name>/', views.file_list_view, name="file_list_by_category"),
    path('ticketing/', views.ticketing_dashboard, name='ticketing_dashboard'),
]
