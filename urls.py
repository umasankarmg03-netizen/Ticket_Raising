"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from .views import home,index, RegisterView,logout_view
from .import views

urlpatterns = [
    path('', home, name='users-home'),
    path('profile/', views.home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile1/', views.profile, name='users-profile'),
    

    path('Model_db/',views.Model_db,name='Model_db'),
    path('chatbot/', views.chatbot_response_view,name='chatbot'),

    path('logout_view/',logout_view,name='logout_view'),
    path('fault_prediction/', views.fault_prediction, name='fault_prediction'),
    path('real-time/', views.real_time_fault_prediction, name='real_time_fault_prediction'),
    path('raise-ticket/<int:system_id>/', views.raise_ticket, name='raise_ticket'),
    
    path('admin-register/', views.admin_register, name='admin-register'),
    path('admin-login/', views.admin_login, name='admin-login'),
    path('admin-logout/', views.admin_logout, name='admin-logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin/ticket/<int:ticket_id>/',views.admin_analyze_ticket,name='admin-analyze-ticket'),
     path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket-detail'),
    path('tickets/', views.user_tickets, name='user-tickets'),






    #Documents
    path('admin/developer/add/', views.admin_add_developer, name='admin-add-developer'),
    path('admin/developers/', views.admin_developer_list, name='admin-developer-list'),
    path('admin/developer/<int:dev_id>/upload/', views.admin_upload_document, name='admin-upload-document'),

    # User routes
    path('developers/', views.senior_developers, name='senior-developers'),
    path('developer/<int:dev_id>/documents/', views.developer_documents, name='developer-documents'),
    path('document/<int:doc_id>/qa/', views.ask_document_question, name='document-qa'),
    

   


]
