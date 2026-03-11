from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.utils import timezone

from .models import (
    User, ServiceCategory, VendorProfile, BrandServiceCenter,
    Appliance, Booking, Review, VideoConsultation
)
from .forms import (
    CustomerRegistrationForm, VendorRegistrationForm, LoginForm,
    ApplianceForm, BookingForm, ReviewForm, VendorProfileForm
)


# ─── Decorators ───────────────────────────────────────────────
def customer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'customer':
            messages.error(request, 'Access restricted to customers.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def vendor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'vendor':
            messages.error(request, 'Access restricted to vendors.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            messages.error(request, 'Access restricted to administrators.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ─── Public Pages ─────────────────────────────────────────────
def home(request):
    categories = ServiceCategory.objects.all()[:8]
    top_vendors = VendorProfile.objects.filter(is_verified=True, is_available=True)[:6]
    brands = BrandServiceCenter.objects.filter(is_active=True)[:6]
    context = {
        'categories': categories,
        'top_vendors': top_vendors,
        'brands': brands,
    }
    return render(request, 'home.html', context)


def service_list(request):
    categories = ServiceCategory.objects.all()
    query = request.GET.get('q', '')
    if query:
        categories = categories.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'service_list.html', {'categories': categories, 'query': query})


def vendor_list(request):
    vendors = VendorProfile.objects.filter(is_available=True)
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    city = request.GET.get('city', '')

    if query:
        vendors = vendors.filter(
            Q(business_name__icontains=query) |
            Q(user__city__icontains=query) |
            Q(services__name__icontains=query)
        ).distinct()
    if category_slug:
        vendors = vendors.filter(services__slug=category_slug)
    if city:
        vendors = vendors.filter(user__city__icontains=city)

    categories = ServiceCategory.objects.all()
    return render(request, 'vendor_list.html', {
        'vendors': vendors,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
        'city': city,
    })


def vendor_detail(request, pk):
    vendor = get_object_or_404(VendorProfile, pk=pk)
    reviews = Review.objects.filter(booking__vendor=vendor).order_by('-created_at')
    return render(request, 'vendor_detail.html', {'vendor': vendor, 'reviews': reviews})


def brand_list(request):
    brands = BrandServiceCenter.objects.filter(is_active=True)
    query = request.GET.get('q', '')
    if query:
        brands = brands.filter(
            Q(brand_name__icontains=query) | Q(city__icontains=query)
        )
    return render(request, 'brand_list.html', {'brands': brands, 'query': query})


def brand_detail(request, slug):
    brand = get_object_or_404(BrandServiceCenter, slug=slug)
    return render(request, 'brand_detail.html', {'brand': brand})


# ─── Authentication ───────────────────────────────────────────
def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your customer account has been created.')
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register.html', {'form': form, 'user_type': 'Customer'})


def register_vendor(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your vendor account has been created.')
            return redirect('vendor_dashboard')
    else:
        form = VendorRegistrationForm()
    return render(request, 'register.html', {'form': form, 'user_type': 'Vendor'})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                if user.role == 'vendor':
                    return redirect('vendor_dashboard')
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


# ─── Appliance Management (Customer) ─────────────────────────
@login_required
@customer_required
def appliance_list(request):
    appliances = Appliance.objects.filter(user=request.user)
    return render(request, 'appliance_list.html', {'appliances': appliances})


@login_required
@customer_required
def appliance_create(request):
    if request.method == 'POST':
        form = ApplianceForm(request.POST)
        if form.is_valid():
            appliance = form.save(commit=False)
            appliance.user = request.user
            appliance.save()
            messages.success(request, 'Appliance added successfully!')
            return redirect('appliance_list')
    else:
        form = ApplianceForm()
    return render(request, 'appliance_form.html', {'form': form, 'action': 'Add'})


@login_required
@customer_required
def appliance_edit(request, pk):
    appliance = get_object_or_404(Appliance, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ApplianceForm(request.POST, instance=appliance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appliance updated!')
            return redirect('appliance_list')
    else:
        form = ApplianceForm(instance=appliance)
    return render(request, 'appliance_form.html', {'form': form, 'action': 'Edit'})


@login_required
@customer_required
def appliance_delete(request, pk):
    appliance = get_object_or_404(Appliance, pk=pk, user=request.user)
    if request.method == 'POST':
        appliance.delete()
        messages.success(request, 'Appliance removed.')
        return redirect('appliance_list')
    return render(request, 'appliance_confirm_delete.html', {'appliance': appliance})


# ─── Booking (Customer) ──────────────────────────────────────
@login_required
@customer_required
def booking_create(request, vendor_pk):
    vendor = get_object_or_404(VendorProfile, pk=vendor_pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.vendor = vendor
            booking.save()
            messages.success(request, f'Booking request sent to {vendor.business_name}!')
            return redirect('booking_list')
    else:
        form = BookingForm()
        form.fields['service'].queryset = vendor.services.all()
    return render(request, 'booking_form.html', {'form': form, 'vendor': vendor})


@login_required
def booking_list(request):
    if request.user.role == 'customer':
        bookings = Booking.objects.filter(customer=request.user)
    elif request.user.role == 'vendor':
        bookings = Booking.objects.filter(vendor=request.user.vendor_profile)
    else:
        bookings = Booking.objects.all()
    return render(request, 'booking_list.html', {'bookings': bookings})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.user.role == 'customer' and booking.customer != request.user:
        messages.error(request, 'Access denied.')
        return redirect('booking_list')
    if request.user.role == 'vendor' and booking.vendor.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('booking_list')
    review_form = None
    if (request.user.role == 'customer' and
        booking.status == 'completed' and
        not hasattr(booking, 'review')):
        review_form = ReviewForm()
    return render(request, 'booking_detail.html', {
        'booking': booking,
        'review_form': review_form,
    })


@login_required
@vendor_required
def booking_update_status(request, pk, status):
    booking = get_object_or_404(Booking, pk=pk, vendor=request.user.vendor_profile)
    if status in dict(Booking.STATUS_CHOICES):
        booking.status = status
        booking.save()
        messages.success(request, f'Booking status updated to {booking.get_status_display()}.')
    return redirect('booking_detail', pk=pk)


@login_required
@customer_required
def review_create(request, booking_pk):
    booking = get_object_or_404(Booking, pk=booking_pk, customer=request.user, status='completed')
    if hasattr(booking, 'review'):
        messages.info(request, 'You have already reviewed this booking.')
        return redirect('booking_detail', pk=booking_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('booking_detail', pk=booking_pk)
    return redirect('booking_detail', pk=booking_pk)


# ─── Video Consultation ──────────────────────────────────────
@login_required
def video_consultation(request, vendor_pk):
    vendor = get_object_or_404(VendorProfile, pk=vendor_pk)
    session, created = VideoConsultation.objects.get_or_create(
        customer=request.user,
        vendor=vendor,
        status='scheduled',
        defaults={'scheduled_at': timezone.now()}
    )
    return render(request, 'video_consultation.html', {
        'vendor': vendor,
        'session': session,
    })


# ─── Vendor Dashboard ────────────────────────────────────────
@login_required
@vendor_required
def vendor_dashboard(request):
    profile = request.user.vendor_profile
    pending_bookings = Booking.objects.filter(vendor=profile, status='pending')
    active_bookings = Booking.objects.filter(vendor=profile, status__in=['accepted', 'in_progress'])
    recent_bookings = Booking.objects.filter(vendor=profile).order_by('-created_at')[:10]
    total_completed = profile.completed_bookings
    total_reviews = profile.total_reviews
    avg_rating = profile.average_rating

    context = {
        'profile': profile,
        'pending_bookings': pending_bookings,
        'active_bookings': active_bookings,
        'recent_bookings': recent_bookings,
        'total_completed': total_completed,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'vendor_dashboard.html', context)


@login_required
@vendor_required
def vendor_profile_edit(request):
    profile = request.user.vendor_profile
    if request.method == 'POST':
        form = VendorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('vendor_dashboard')
    else:
        form = VendorProfileForm(instance=profile)
    return render(request, 'vendor_profile_edit.html', {'form': form})


# ─── Admin Dashboard ─────────────────────────────────────────
@login_required
@admin_required
def admin_dashboard(request):
    total_customers = User.objects.filter(role='customer').count()
    total_vendors = User.objects.filter(role='vendor').count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    unverified_vendors = VendorProfile.objects.filter(is_verified=False)
    recent_bookings = Booking.objects.order_by('-created_at')[:20]
    categories = ServiceCategory.objects.all()

    context = {
        'total_customers': total_customers,
        'total_vendors': total_vendors,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'unverified_vendors': unverified_vendors,
        'recent_bookings': recent_bookings,
        'categories': categories,
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
@admin_required
def admin_verify_vendor(request, pk):
    vendor = get_object_or_404(VendorProfile, pk=pk)
    vendor.is_verified = True
    vendor.save()
    messages.success(request, f'{vendor.business_name} has been verified!')
    return redirect('admin_dashboard')


@login_required
@admin_required
def admin_manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(role=role_filter)
    return render(request, 'admin_manage_users.html', {'users': users, 'role_filter': role_filter})
