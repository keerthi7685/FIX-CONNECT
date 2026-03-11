from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    @property
    def is_customer(self):
        return self.role == 'customer'

    @property
    def is_vendor(self):
        return self.role == 'vendor'

    @property
    def is_admin_user(self):
        return self.role == 'admin'


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-tools')  # FontAwesome icon class

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    business_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    services = models.ManyToManyField(ServiceCategory, related_name='vendors')
    experience_years = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name

    @property
    def average_rating(self):
        reviews = Review.objects.filter(booking__vendor=self)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0.0

    @property
    def total_reviews(self):
        return Review.objects.filter(booking__vendor=self).count()

    @property
    def completed_bookings(self):
        return self.bookings.filter(status='completed').count()


class BrandServiceCenter(models.Model):
    brand_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    services = models.ManyToManyField(ServiceCategory, blank=True, related_name='brand_centers')
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name


class Appliance(models.Model):
    APPLIANCE_TYPES = (
        ('ac', 'Air Conditioner'),
        ('refrigerator', 'Refrigerator'),
        ('washing_machine', 'Washing Machine'),
        ('tv', 'Television'),
        ('microwave', 'Microwave'),
        ('water_heater', 'Water Heater'),
        ('dishwasher', 'Dishwasher'),
        ('other', 'Other'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appliances')
    appliance_type = models.CharField(max_length=20, choices=APPLIANCE_TYPES)
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    warranty_end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_appliance_type_display()} - {self.brand}"

    @property
    def is_under_warranty(self):
        if self.warranty_end_date:
            from django.utils import timezone
            return self.warranty_end_date >= timezone.now().date()
        return False


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_bookings')
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.pk} - {self.customer.username} → {self.vendor.business_name}"


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Booking #{self.booking.pk} - {self.rating}★"


class VideoConsultation(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='video_sessions', null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_as_customer')
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='video_sessions')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video Call #{self.pk} - {self.customer.username} ↔ {self.vendor.business_name}"
