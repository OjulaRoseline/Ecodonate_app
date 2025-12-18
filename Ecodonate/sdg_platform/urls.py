# sdg_platform/urls.py (Replace the old donate paths)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'), 
    # NEW REAL DARAAJA ENDPOINTS
    path('donate/mpesa_stk/<int:pk>/', views.mpesa_stk_push, name='mpesa_stk_push'),
    path('donate/callback/', views.mpesa_callback, name='mpesa_callback'), # This is the secure endpoint
    # 1. Starts the donation (form submission)
    path('donate/start/<int:pk>/', views.donate_start, name='donate_start'),
    # 2. Confirms/Simulates the payment (uses session data)
    path('donate/confirm/', views.donate_confirm, name='donate_confirm'),
    # 3. Completes the transaction (database update)
    path('donate/complete/', views.donate_complete, name='donate_complete'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
]