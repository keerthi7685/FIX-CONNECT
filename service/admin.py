from django.contrib import admin
from .models import (
    User, ServiceCategory, VendorProfile, BrandServiceCenter,
    Appliance, Booking, Review, VideoConsultation
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'phone', 'city', 'is_active']
    list_filter = ['role', 'is_active', 'city']
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'user', 'experience_years', 'hourly_rate', 'is_verified', 'is_available']
    list_filter = ['is_verified', 'is_available']
    search_fields = ['business_name', 'user__username']


@admin.register(BrandServiceCenter)
class BrandServiceCenterAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'phone', 'email', 'city', 'is_active']
    list_filter = ['is_active', 'city']
    prepopulated_fields = {'slug': ('brand_name',)}


@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    list_display = ['appliance_type', 'brand', 'user', 'purchase_date', 'warranty_end_date']
    list_filter = ['appliance_type', 'brand']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'vendor', 'service', 'scheduled_date', 'status']
    list_filter = ['status', 'scheduled_date']
    search_fields = ['customer__username', 'vendor__business_name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['booking', 'rating', 'created_at']
    list_filter = ['rating']


@admin.register(VideoConsultation)
class VideoConsultationAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'vendor', 'status', 'scheduled_at']
    list_filter = ['status']
