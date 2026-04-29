"""
URL configuration for mindharbor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wellness import views

urlpatterns = [
    path('', views.signin_view, name='home'),   # Root URL goes to Sign In

    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('counselor-dashboard/', views.counselor_dashboard, name='counselor_dashboard'),

    # CRUD
    path('add-resource/', views.add_resource, name='add_resource'),
    path('edit-resource/<int:pk>/', views.edit_resource, name='edit_resource'),
    path('delete-resource/<int:pk>/', views.delete_resource, name='delete_resource'),

    path('add-session/', views.add_session, name='add_session'),
    path('edit-session/<int:pk>/', views.edit_session, name='edit_session'),
    path('delete-session/<int:pk>/', views.delete_session, name='delete_session'),

    path('add-support/', views.add_support, name='add_support'),
    path('edit-support/<int:pk>/', views.edit_support, name='edit_support'),
    path('delete-support/<int:pk>/', views.delete_support, name='delete_support'),

    path('resources/', views.resources_list, name='resources_list'),
    path('counseling/', views.counseling_list, name='counseling_list'),
    path('support/', views.support_list, name='support_list'),
]