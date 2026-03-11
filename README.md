# Consult — Home Service Platform

> **The all-in-one platform to discover, consult, and book home service professionals.**

Consult is a full-stack web application built with Django that connects homeowners with reliable local technicians and official brand service centers. Users can search for services, compare vendors by ratings, consult experts via live video, track appliance warranties, and book home maintenance services — all from a single platform.

---

## Table of Contents

1. [Purpose of the Application](#1-purpose-of-the-application)
2. [Problems Solved](#2-problems-solved)
3. [Key Features](#3-key-features)
4. [User Roles](#4-user-roles)
5. [Application Workflow](#5-application-workflow)
6. [Tech Stack](#6-tech-stack)
7. [Technical Architecture](#7-technical-architecture)
8. [Project Structure](#8-project-structure)
9. [Installation & Setup](#9-installation--setup)
10. [User Guide](#10-user-guide)
11. [Login Credentials](#11-login-credentials)
12. [Database Models](#12-database-models)
13. [URL Endpoints](#13-url-endpoints)
14. [Admin Panel](#14-admin-panel)
15. [Design System](#15-design-system)

---

## 1. Purpose of the Application

The application is designed to help homeowners **quickly find and connect with reliable home maintenance service providers**. It provides a single platform where users can:

- **Find nearby local technicians** (plumbers, electricians, carpenters, etc.)
- **Contact official brand service centers** (LG, Samsung, Daikin, Voltas)
- **Consult vendors through live video** before booking
- **Book home maintenance services** with date/time selection
- **Track appliance warranties** and get reminded about free services
- **Rate and review** service providers for community trust

---

## 2. Problems Solved

| Problem | How Consult Solves It |
|---|---|
| Manually searching for technicians | Centralized vendor directory with search and filters |
| Depending on neighbors for random contacts | Curated, verified vendor profiles with ratings |
| Not knowing which technician is reliable | Community-driven rating and review system |
| No visibility into technician availability | Real-time availability status on vendor profiles |
| Contacting local vendors for warranty items | Brand service center integration with warranty tracking |
| Extra costs from unnecessary repairs | Live video consultation for remote diagnosis |
| No booking history or service tracking | Complete booking management with status tracking |

---

## 3. Key Features

### 3.1 Service Search & Discovery
- Browse 8+ service categories (Plumbing, Electrical, AC Repair, Appliance Repair, Carpentry, Painting, Cleaning, Roofing)
- Full-text search across vendors, services, and locations
- Filter vendors by category, city, and keyword

### 3.2 Vendor Discovery
- View all available local service providers near the user
- Each vendor profile displays:
  - Business name and description
  - Star rating (1-5) and total reviews
  - Years of experience
  - Hourly rate (₹)
  - Number of completed jobs
  - Services offered (category tags)
  - City and area location
  - Verification badge (for admin-verified vendors)
  - Availability status (Available / Unavailable)

### 3.3 Vendor Rating & Review System
- After a booking is marked as **completed**, the customer can leave a review
- Reviews include a **1-5 star rating** and an optional **text comment**
- Interactive star-rating widget powered by JavaScript
- Average rating is calculated and displayed on vendor cards and profiles
- Reviews are publicly visible on vendor detail pages

### 3.4 Brand Service Center Integration
- Directory of official brand service centers (LG, Samsung, Daikin, Voltas)
- Each brand listing includes:
  - Toll-free contact number
  - Email address
  - Official website link
  - Address and city
  - Services covered
- Helps users **avoid unnecessary expenses** by directing them to warranty-eligible services

### 3.5 Appliance Management
- Customers can register their home appliances with details:
  - Appliance type (AC, Refrigerator, Washing Machine, TV, Microwave, Water Heater, Dishwasher, Other)
  - Brand name
  - Model number
  - Purchase date
  - Warranty end date
  - Additional notes
- The system automatically checks and displays:
  - **Under Warranty** badge (green) if warranty is still active
  - **Warranty Expired** badge (red) if warranty has passed
- Full CRUD operations: Add, Edit, Delete appliances

### 3.6 Live Video Consultation
- Customers can start a **live video call** with any vendor
- Uses the browser's native `getUserMedia` API to access camera and microphone
- During the video session:
  - Users can show the issue directly through their camera
  - Vendors can diagnose the problem remotely
  - Vendors can give repair advice
  - Users can decide whether to book an on-site service
- Video controls include: Start Camera, Mute/Unmute, and End Call
- Saves time and eliminates unnecessary on-site visits

### 3.7 Service Booking
- Customers can book a technician directly through the platform
- Booking form includes:
  - Service category selection (filtered to vendor's offerings)
  - Issue description
  - Preferred date and time
  - Service address
- Booking status lifecycle: **Pending → Accepted → In Progress → Completed**
- Vendors can also **decline** (cancel) a booking

### 3.8 Booking History
- Customers can view all their past and current bookings
- Vendors can view all incoming service requests
- Booking details include:
  - Service type
  - Vendor/customer information
  - Scheduled date and time
  - Current status with color-coded badges
  - Issue description
  - Review (if completed)

### 3.9 Vendor Dashboard
- Dedicated dashboard for vendor accounts showing:
  - **Statistics**: Jobs completed, pending requests, active jobs, average rating, total reviews
  - **Pending Requests**: Table with Accept/Decline actions
  - **Active Jobs**: Table with Start/Complete actions
  - **Recent Bookings**: Full history table
- Quick links to edit profile and view all bookings

### 3.10 Admin Dashboard
- Administrative panel for platform management:
  - **Platform Statistics**: Total customers, vendors, bookings, pending bookings, categories
  - **Vendor Verification**: List of unverified vendors with one-click verification
  - **Service Categories**: Overview with vendor counts per category
  - **User Management**: Full user listing with role-based filtering
  - **Recent Bookings**: Platform-wide booking activity feed
- Links to Django's built-in admin for advanced management

---

## 4. User Roles

The application supports **three distinct user roles**, each with specific permissions:

### 4.1 Customer
| Capability | Description |
|---|---|
| Browse services | Search and filter service categories |
| View vendors | View vendor profiles, ratings, and reviews |
| Book services | Create booking requests with date/time |
| Video consultation | Start live video calls with vendors |
| Manage appliances | Add, edit, delete home appliances with warranty tracking |
| Leave reviews | Rate and review completed bookings |
| View booking history | Track all past and current service requests |

### 4.2 Vendor
| Capability | Description |
|---|---|
| Dashboard | View stats, pending/active jobs, history |
| Manage bookings | Accept, decline, start, and complete jobs |
| Edit profile | Update business info, services, hourly rate, availability |
| Video consultation | Receive video calls from customers |

### 4.3 Admin
| Capability | Description |
|---|---|
| Platform overview | View all platform statistics |
| Verify vendors | Approve vendor registrations |
| Manage users | View and filter all platform users |
| Manage categories | Administer service categories via Django admin |
| Monitor bookings | View all booking activity across the platform |

---

## 5. Application Workflow

```
Step 1: User opens the application
    │
Step 2: User browses or searches for a service category
    │
Step 3: If the issue involves appliances, user checks:
    │   ├── Appliance type & brand
    │   └── Warranty status (via My Appliances)
    │
Step 4: System shows:
    │   ├── Official brand service centers (for warranty items)
    │   └── Local technicians (for general repairs)
    │
Step 5: User can:
    │   ├── Start a video consultation (for remote diagnosis)
    │   └── Directly book an on-site service
    │
Step 6: Vendor receives the request and accepts/declines
    │
Step 7: Vendor completes the work and marks booking as done
    │
Step 8: Customer provides a star rating and review
```

---

## 6. Tech Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Backend Framework** | Django | 6.0.3 | Web framework, ORM, auth, admin |
| **Language** | Python | 3.14 | Server-side logic |
| **Database** | SQLite | 3 | Development database (file-based) |
| **Image Processing** | Pillow | 12.1.1 | ImageField support for profiles/logos |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) | — | UI rendering and interactivity |
| **CSS Architecture** | Custom Design System | — | Dark glassmorphism with CSS variables |
| **Typography** | Google Fonts (Inter) | — | Modern sans-serif font family |
| **Icons** | Font Awesome | 6.5.1 | 200+ icons throughout the UI |
| **Video** | WebRTC / getUserMedia API | — | Browser-native video consultation |
| **Template Engine** | Django Template Language (DTL) | — | Server-side HTML rendering |

---

## 7. Technical Architecture

### 7.1 Design Pattern
- **MVT (Model-View-Template)** — Django's variant of MVC
  - **Models**: 8 data models in `service/models.py`
  - **Views**: 25+ view functions in `service/views.py`
  - **Templates**: 16 HTML templates in `templates/`

### 7.2 Authentication System
- **Custom User Model**: Extends Django's `AbstractUser` with `role`, `phone`, `city`, `area`, and `profile_image` fields
- **Role-based access control**: Custom decorators (`@customer_required`, `@vendor_required`, `@admin_required`) restrict views by user role
- **Session-based authentication**: Uses Django's built-in session middleware

### 7.3 Database Design
- **Relational schema** with proper foreign keys and one-to-one/many-to-many relationships
- **Computed properties** using `@property` decorators (e.g., `average_rating`, `is_under_warranty`)
- **Soft validation** using Django's `MinValueValidator` / `MaxValueValidator`
- **Auto-timestamps** using `auto_now_add` and `auto_now` fields

### 7.4 Form Handling
- **Django ModelForms** with custom widgets and CSS class injection
- **Custom registration forms** extending `UserCreationForm` for Customer and Vendor signup
- **Server-side validation** with inline error display

### 7.5 Frontend Architecture
- **CSS Custom Properties** (CSS Variables) for a centralized design token system
- **Glassmorphism effect**: `backdrop-filter: blur()` with semi-transparent backgrounds
- **Gradient system**: Multi-stop linear gradients for buttons, badges, and accents
- **Intersection Observer API**: Scroll-triggered fade-in animations for cards
- **Responsive design**: CSS Grid + media queries for mobile, tablet, and desktop layouts

### 7.6 Video Consultation
- **getUserMedia API**: Accesses the user's camera and microphone through the browser
- **UI-only MVP**: Camera preview and controls are functional; peer-to-peer signaling (WebRTC full stack) requires a signaling server for production

### 7.7 Management Commands
- **Custom `seed_data` command**: Populates the database with realistic sample data (categories, users, vendors, brand centers)

---

## 8. Project Structure

```
my_project/
│
├── consult/                        # Django project configuration
│   ├── __init__.py
│   ├── settings.py                 # Project settings (DB, auth, static, templates)
│   ├── urls.py                     # Root URL configuration
│   ├── wsgi.py                     # WSGI entry point
│   └── asgi.py                     # ASGI entry point
│
├── service/                        # Main application
│   ├── __init__.py
│   ├── models.py                   # 8 data models
│   ├── views.py                    # 25+ view functions
│   ├── forms.py                    # 7 form classes
│   ├── admin.py                    # Admin registrations with list views
│   ├── urls.py                     # 20+ URL patterns
│   ├── apps.py                     # App configuration
│   ├── migrations/                 # Database migration files
│   │   └── 0001_initial.py
│   └── management/
│       └── commands/
│           └── seed_data.py        # Database seeding command
│
├── templates/                      # HTML templates (16 files)
│   ├── base.html                   # Base layout (nav, footer, messages)
│   ├── home.html                   # Homepage (hero, categories, vendors, brands)
│   ├── login.html                  # Login form
│   ├── register.html               # Registration form (Customer/Vendor)
│   ├── service_list.html           # Service category listing
│   ├── vendor_list.html            # Vendor discovery with filters
│   ├── vendor_detail.html          # Vendor profile with reviews
│   ├── brand_list.html             # Brand service center listing
│   ├── brand_detail.html           # Brand center detail page
│   ├── appliance_list.html         # User's appliances with warranty status
│   ├── appliance_form.html         # Add/edit appliance form
│   ├── appliance_confirm_delete.html # Delete confirmation
│   ├── booking_form.html           # Create booking form
│   ├── booking_list.html           # Booking history table
│   ├── booking_detail.html         # Booking detail with actions
│   ├── video_consultation.html     # Video call interface
│   ├── vendor_dashboard.html       # Vendor stats and job management
│   ├── vendor_profile_edit.html    # Edit vendor profile form
│   ├── admin_dashboard.html        # Admin platform management
│   └── admin_manage_users.html     # Admin user listing
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css               # Complete design system (900+ lines)
│   ├── js/
│   │   └── main.js                 # Interactive features
│   └── images/                     # Image assets
│
├── media/                          # User-uploaded files (profiles, logos)
├── env/                            # Python virtual environment
├── db.sqlite3                      # SQLite database file
├── manage.py                       # Django management script
└── README.md                       # This file
```

---

## 9. Installation & Setup

### Prerequisites
- Python 3.10 or higher installed on your system
- pip (Python package manager)

### Step-by-Step Setup

**1. Navigate to the project directory**
```bash
cd c:\Users\LENOVO\Desktop\my_project
```

**2. Create and activate the virtual environment**
```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

**3. Install dependencies**
```bash
pip install django Pillow
```

**4. Run database migrations**
```bash
python manage.py makemigrations service
python manage.py migrate
```

**5. Seed the database with sample data**
```bash
python manage.py seed_data
```

**6. Start the development server**
```bash
python manage.py runserver
```

**7. Open in your browser**
```
http://127.0.0.1:8000/
```

---

## 10. User Guide

### 10.1 For Customers

#### Registering an Account
1. Click **"Sign Up"** in the top navigation bar
2. Fill in your details: username, name, email, phone, city, area, and password
3. Click **"Create Customer Account"**
4. You will be automatically logged in and redirected to the homepage

#### Finding a Service
1. Use the **search bar** on the homepage to search for services (e.g., "plumber", "AC repair")
2. Or click **"Services"** in the navbar to browse all categories
3. Click on a category to see vendors offering that service

#### Discovering Vendors
1. Click **"Vendors"** in the navbar to see all available professionals
2. Use the **filter bar** to narrow results by:
   - Keyword (vendor name, service)
   - Category (dropdown)
   - City (text input)
3. Each vendor card shows their rating, experience, hourly rate, and services

#### Viewing a Vendor Profile
1. Click **"View Profile"** on any vendor card
2. The profile page shows detailed information, all reviews, and action buttons
3. From here you can **Book Service** or start a **Video Consultation**

#### Starting a Video Consultation
1. Navigate to a vendor's profile
2. Click **"Video Consult"** or the video icon button
3. On the video page, click the **camera button** to start your camera
4. Show the issue to the vendor through your camera
5. Use the **mute button** to toggle audio
6. Click the **red phone button** to end the call
7. After the consultation, you can decide to book an on-site service

#### Booking a Service
1. From a vendor profile or vendor listing, click **"Book"** or **"Book Service"**
2. Fill in the booking form:
   - Select the service type
   - Describe the issue
   - Choose a preferred date and time
   - Enter your service address
3. Click **"Confirm Booking"**
4. The vendor will receive your request and can accept or decline

#### Managing Your Bookings
1. Click **"Bookings"** in the navbar
2. View all your bookings with their current status:
   - **Pending**: Waiting for vendor response
   - **Accepted**: Vendor confirmed your request
   - **In Progress**: Vendor is working on the job
   - **Completed**: Job is finished
   - **Cancelled**: Booking was declined
3. Click **"View"** on any booking for full details

#### Leaving a Review
1. After a booking is marked as **Completed**, open the booking detail page
2. You'll see a **"Leave a Review"** form at the bottom
3. Click on the stars to select your rating (1-5)
4. Optionally write a comment
5. Click **"Submit Review"**

#### Managing Appliances
1. Click **"My Appliances"** in the navbar
2. Click **"Add Appliance"** to register a new appliance
3. Fill in the details:
   - Appliance type
   - Brand name
   - Model number (optional)
   - Purchase date (optional)
   - Warranty end date (optional)
   - Notes (optional)
4. The system automatically shows warranty status badges
5. Use **Edit** and **Delete** buttons to manage your appliances

---

### 10.2 For Vendors

#### Registering as a Vendor
1. On the login page, click **"Register as Vendor"**
2. Fill in your details plus business information:
   - Business/Service name
   - Description of your services
   - Years of experience
   - Hourly rate (₹)
3. Click **"Create Vendor Account"**
4. You will be redirected to your Vendor Dashboard

#### Using the Vendor Dashboard
1. Click **"Dashboard"** in the navbar
2. Your dashboard shows:
   - **Stats cards**: Jobs completed, pending requests, active jobs, rating, reviews
   - **Pending Requests**: New booking requests you need to respond to
   - **Active Jobs**: Currently ongoing service requests
   - **Recent Bookings**: Your complete booking history

#### Managing Booking Requests
1. When a customer books your service, it appears in the **Pending Requests** section
2. Click **"Accept"** to confirm the booking or **"Decline"** to reject it
3. For accepted bookings, click **"Start"** when you begin working on the job
4. After completing the work, click **"Complete"** to mark it as done

#### Editing Your Profile
1. From the dashboard, click **"Edit Profile"**
2. Update your:
   - Business name
   - Description
   - Services offered (checkboxes)
   - Years of experience
   - Hourly rate
   - Availability toggle
3. Click **"Save Changes"**

---

### 10.3 For Admins

#### Accessing the Admin Dashboard
1. Log in with an admin account
2. Click **"Admin"** in the navbar
3. The dashboard shows platform-wide statistics and management tools

#### Verifying Vendors
1. The **Unverified Vendors** section lists vendors awaiting verification
2. Click **"Verify"** to approve a vendor (they get a verified badge)
3. Click **"View"** to review their profile before verification

#### Managing Users
1. Click **"Manage Users"** from the admin dashboard
2. Use the role filter dropdown to view Customers, Vendors, or Admins
3. The table shows username, name, email, role, city, join date, and active status

#### Advanced Administration
1. Click **"Django Admin"** to access the full Django admin interface at `/admin/`
2. From there you can:
   - Add, edit, or delete any model records
   - Manage service categories
   - View and modify booking records
   - Manage brand service centers

---

## 11. Login Credentials

### Pre-seeded Accounts

| Role | Username | Password | Details |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Platform administrator, Mumbai |
| **Customer** | `customer1` | `customer123` | Rahul Sharma, Mumbai - Andheri West |
| **Vendor 1** | `vendor1` | `vendor123` | RK Plumbing Solutions, Mumbai - Bandra, 15yr exp, ₹350/hr, Verified |
| **Vendor 2** | `vendor2` | `vendor123` | SP Electrical Works, Mumbai - Powai, 12yr exp, ₹400/hr, Verified |
| **Vendor 3** | `vendor3` | `vendor123` | CoolAir AC Services, Delhi - Dwarka, 8yr exp, ₹500/hr, Verified |
| **Vendor 4** | `vendor4` | `vendor123` | HomeFixAll, Bangalore - Whitefield, 10yr exp, ₹300/hr, Unverified |
| **Vendor 5** | `vendor5` | `vendor123` | CleanStar Services, Mumbai - Juhu, 5yr exp, ₹250/hr, Verified |

### Django Admin Panel
- **URL**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`

---

## 12. Database Models

| Model | Description | Key Fields |
|---|---|---|
| **User** | Custom user extending AbstractUser | `role`, `phone`, `city`, `area`, `profile_image` |
| **ServiceCategory** | Service types (Plumbing, Electrical, etc.) | `name`, `slug`, `description`, `icon` |
| **VendorProfile** | Vendor business profiles (1:1 with User) | `business_name`, `services` (M2M), `experience_years`, `hourly_rate`, `is_verified`, `is_available` |
| **BrandServiceCenter** | Official brand service contacts | `brand_name`, `phone`, `email`, `website`, `address`, `services` (M2M) |
| **Appliance** | Customer's home appliances | `appliance_type`, `brand`, `model_number`, `purchase_date`, `warranty_end_date` |
| **Booking** | Service booking requests | `customer` (FK), `vendor` (FK), `service` (FK), `scheduled_date`, `scheduled_time`, `status` |
| **Review** | Customer ratings for completed bookings | `booking` (1:1), `rating` (1-5), `comment` |
| **VideoConsultation** | Video call session records | `customer` (FK), `vendor` (FK), `booking` (FK), `status`, `scheduled_at` |

---

## 13. URL Endpoints

### Public Pages
| URL | View | Description |
|---|---|---|
| `/` | `home` | Homepage with hero, categories, vendors, brands |
| `/services/` | `service_list` | Browse service categories |
| `/vendors/` | `vendor_list` | Discover vendors with filters |
| `/vendors/<id>/` | `vendor_detail` | Vendor profile and reviews |
| `/brands/` | `brand_list` | Brand service center directory |
| `/brands/<slug>/` | `brand_detail` | Brand center detail page |

### Authentication
| URL | View | Description |
|---|---|---|
| `/register/` | `register_customer` | Customer registration |
| `/register/vendor/` | `register_vendor` | Vendor registration |
| `/login/` | `user_login` | Login page |
| `/logout/` | `user_logout` | Logout action |

### Customer Features
| URL | View | Description |
|---|---|---|
| `/appliances/` | `appliance_list` | View registered appliances |
| `/appliances/add/` | `appliance_create` | Add new appliance |
| `/appliances/<id>/edit/` | `appliance_edit` | Edit appliance |
| `/appliances/<id>/delete/` | `appliance_delete` | Delete appliance |
| `/book/<vendor_id>/` | `booking_create` | Book a vendor's service |
| `/bookings/` | `booking_list` | Booking history |
| `/bookings/<id>/` | `booking_detail` | Booking details |
| `/bookings/<id>/review/` | `review_create` | Submit a review |
| `/video/<vendor_id>/` | `video_consultation` | Video call interface |

### Vendor Features
| URL | View | Description |
|---|---|---|
| `/dashboard/` | `vendor_dashboard` | Vendor stats and job management |
| `/dashboard/profile/` | `vendor_profile_edit` | Edit vendor profile |
| `/bookings/<id>/status/<status>/` | `booking_update_status` | Update booking status |

### Admin Features
| URL | View | Description |
|---|---|---|
| `/admin-panel/` | `admin_dashboard` | Platform administration |
| `/admin-panel/verify/<id>/` | `admin_verify_vendor` | Verify a vendor |
| `/admin-panel/users/` | `admin_manage_users` | Manage platform users |
| `/admin/` | Django Admin | Built-in Django admin interface |

---

## 14. Admin Panel

Django's built-in admin panel is fully configured at `/admin/` with the following registered models:

- **Users** — List display: username, email, role, phone, city, active status. Filterable by role, active status, city. Searchable by username, email, name.
- **Service Categories** — Auto-generated slugs from name. Displays name, slug, icon.
- **Vendor Profiles** — Filterable by verified/available status. Searchable by business name.
- **Brand Service Centers** — Filterable by active status and city. Auto-generated slugs.
- **Appliances** — Filterable by type and brand. Shows user, purchase date, warranty.
- **Bookings** — Filterable by status and date. Searchable by customer/vendor.
- **Reviews** — Filterable by rating. Shows booking and creation date.
- **Video Consultations** — Filterable by status. Shows participants and schedule.

---

## 15. Design System

The application uses a **dark glassmorphism** design system with the following characteristics:

- **Color Palette**: Deep navy backgrounds (`#0a0e1a`, `#111827`) with indigo-violet-cyan gradient accents
- **Glassmorphism**: Semi-transparent cards with `backdrop-filter: blur()` effects
- **Typography**: Inter font family (Google Fonts) with weights 300-800
- **Animations**: CSS keyframe animations for floating backgrounds, fade-in-up scroll effects, and slide-in notifications
- **Responsive**: Full mobile/tablet/desktop support via CSS Grid and media queries at 1024px, 768px, and 480px breakpoints
- **Icons**: Font Awesome 6.5 with 200+ icons used across the interface
- **Design Tokens**: 30+ CSS custom properties for consistent theming

---

## License

This project is built for educational and development purposes.

---

**Built with Django by a professional fullstack developer.**
