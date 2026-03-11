from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('services/', views.service_list, name='service_list'),
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('brands/', views.brand_list, name='brand_list'),
    path('brands/<slug:slug>/', views.brand_detail, name='brand_detail'),

    # Auth
    path('register/', views.register_customer, name='register_customer'),
    path('register/vendor/', views.register_vendor, name='register_vendor'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Appliances (Customer)
    path('appliances/', views.appliance_list, name='appliance_list'),
    path('appliances/add/', views.appliance_create, name='appliance_create'),
    path('appliances/<int:pk>/edit/', views.appliance_edit, name='appliance_edit'),
    path('appliances/<int:pk>/delete/', views.appliance_delete, name='appliance_delete'),

    # Bookings
    path('book/<int:vendor_pk>/', views.booking_create, name='booking_create'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:pk>/status/<str:status>/', views.booking_update_status, name='booking_update_status'),
    path('bookings/<int:booking_pk>/review/', views.review_create, name='review_create'),

    # Video Consultation
    path('video/<int:vendor_pk>/', views.video_consultation, name='video_consultation'),

    # Vendor Dashboard
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('dashboard/profile/', views.vendor_profile_edit, name='vendor_profile_edit'),

    # Admin Dashboard
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/verify/<int:pk>/', views.admin_verify_vendor, name='admin_verify_vendor'),
    path('admin-panel/users/', views.admin_manage_users, name='admin_manage_users'),
]
