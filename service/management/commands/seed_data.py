from django.core.management.base import BaseCommand
from service.models import (
    User, ServiceCategory, VendorProfile, BrandServiceCenter
)


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...\n')

        # ─── Service Categories ───────────────────────────
        categories_data = [
            ('Plumbing', 'plumbing', 'Pipe repair, leak fixing, bathroom fitting', 'fas fa-faucet'),
            ('Electrical', 'electrical', 'Wiring, switch repair, electrical installations', 'fas fa-bolt'),
            ('AC Repair', 'ac-repair', 'AC servicing, gas refill, installation', 'fas fa-snowflake'),
            ('Appliance Repair', 'appliance-repair', 'Washing machine, refrigerator, microwave repair', 'fas fa-tools'),
            ('Carpentry', 'carpentry', 'Furniture repair, door fixing, woodwork', 'fas fa-hammer'),
            ('Painting', 'painting', 'Interior and exterior painting services', 'fas fa-paint-roller'),
            ('Cleaning', 'cleaning', 'Deep cleaning, sanitization, pest control', 'fas fa-broom'),
            ('Roofing', 'roofing', 'Roof repair, waterproofing, leak sealing', 'fas fa-home'),
        ]

        categories = {}
        for name, slug, desc, icon in categories_data:
            cat, created = ServiceCategory.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': desc, 'icon': icon}
            )
            categories[slug] = cat
            status = 'created' if created else 'exists'
            self.stdout.write(f'  Category: {name} [{status}]')

        # ─── Admin User ───────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@consult.com',
                password='admin123',
                role='admin',
                first_name='Admin',
                last_name='User',
                city='Mumbai',
            )
            self.stdout.write('  Admin user: admin / admin123 [created]')
        else:
            self.stdout.write('  Admin user: admin [exists]')

        # ─── Sample Customer ─────────────────────────────
        if not User.objects.filter(username='customer1').exists():
            customer = User.objects.create_user(
                username='customer1',
                email='customer@example.com',
                password='customer123',
                role='customer',
                first_name='Rahul',
                last_name='Sharma',
                phone='9876543210',
                city='Mumbai',
                area='Andheri West',
            )
            self.stdout.write('  Customer: customer1 / customer123 [created]')

        # ─── Sample Vendors ──────────────────────────────
        vendors_data = [
            ('vendor1', 'Ravi', 'Kumar', 'RK Plumbing Solutions', 'Expert plumbing services for residential and commercial properties. 15+ years of trusted service.', 15, 350, 'Mumbai', 'Bandra', ['plumbing'], True),
            ('vendor2', 'Suresh', 'Patel', 'SP Electrical Works', 'Certified electrician providing safe and reliable electrical solutions for homes and offices.', 12, 400, 'Mumbai', 'Powai', ['electrical'], True),
            ('vendor3', 'Amit', 'Singh', 'CoolAir AC Services', 'Specialized in all brands of AC repair, servicing, and installation.', 8, 500, 'Delhi', 'Dwarka', ['ac-repair', 'appliance-repair'], True),
            ('vendor4', 'Manoj', 'Verma', 'HomeFixAll', 'Multi-skilled technician for all your home repair needs.', 10, 300, 'Bangalore', 'Whitefield', ['carpentry', 'plumbing', 'painting'], False),
            ('vendor5', 'Deepak', 'Joshi', 'CleanStar Services', 'Professional deep cleaning and sanitization services.', 5, 250, 'Mumbai', 'Juhu', ['cleaning'], True),
        ]

        for uname, fname, lname, bname, desc, exp, rate, city, area, svc_slugs, verified in vendors_data:
            if not User.objects.filter(username=uname).exists():
                user = User.objects.create_user(
                    username=uname, email=f'{uname}@example.com', password='vendor123',
                    role='vendor', first_name=fname, last_name=lname,
                    phone='98765' + uname[-1] * 5, city=city, area=area,
                )
                profile = VendorProfile.objects.create(
                    user=user, business_name=bname, description=desc,
                    experience_years=exp, hourly_rate=rate, is_verified=verified,
                )
                for s in svc_slugs:
                    if s in categories:
                        profile.services.add(categories[s])
                self.stdout.write(f'  Vendor: {uname} / vendor123 [{bname}] [created]')
            else:
                self.stdout.write(f'  Vendor: {uname} [exists]')

        # ─── Brand Service Centers ────────────────────────
        brands_data = [
            ('LG', 'lg', 'LG Electronics official service center for TVs, ACs, refrigerators, and washing machines.', '1800-315-9999', 'lg.service@lg.com', 'https://www.lg.com/in/support', 'Mumbai', ['ac-repair', 'appliance-repair']),
            ('Samsung', 'samsung', 'Samsung Electronics authorized service center for all Samsung appliances and electronics.', '1800-407-267864', 'support@samsung.com', 'https://www.samsung.com/in/support', 'Delhi', ['ac-repair', 'appliance-repair']),
            ('Daikin', 'daikin', 'Daikin Industries official service for air conditioning systems.', '1800-209-1616', 'service@daikin.com', 'https://www.daikin.co.in', 'Bangalore', ['ac-repair']),
            ('Voltas', 'voltas', 'Voltas official service center — ACs, air coolers, and commercial refrigeration.', '1800-266-4555', 'care@voltas.com', 'https://www.voltas.com', 'Mumbai', ['ac-repair']),
        ]

        for bname, slug, desc, phone, email, website, city, svc_slugs in brands_data:
            brand, created = BrandServiceCenter.objects.get_or_create(
                slug=slug,
                defaults={
                    'brand_name': bname, 'description': desc, 'phone': phone,
                    'email': email, 'website': website, 'city': city,
                }
            )
            if created:
                for s in svc_slugs:
                    if s in categories:
                        brand.services.add(categories[s])
            status = 'created' if created else 'exists'
            self.stdout.write(f'  Brand: {bname} [{status}]')

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('   Credentials:'))
        self.stdout.write(self.style.SUCCESS('   Admin:    admin / admin123'))
        self.stdout.write(self.style.SUCCESS('   Customer: customer1 / customer123'))
        self.stdout.write(self.style.SUCCESS('   Vendors:  vendor1-5 / vendor123'))
