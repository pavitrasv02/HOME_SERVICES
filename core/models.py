from django.db import models

# Service Type Choices
SERVICE_TYPE_CHOICES = [
    ('cleaning', 'Cleaning Services'),
    ('maintenance', 'Maintenance & Repairs'),
    ('gardening', 'Gardening & Landscaping'),
    ('automation', 'Home Automation'),
    ('security', 'Security Services'),
    ('cooking', 'Cooking Services'),
]

# Service-specific Options
CLEANING_OPTIONS = [
    ('regular', 'Regular House Cleaning'),
    ('deep', 'Deep Cleaning'),
    ('carpet', 'Carpet and Upholstery Cleaning'),
    ('window', 'Window Cleaning'),
    ('move', 'Move-in/Move-out Cleaning'),
]

MAINTENANCE_OPTIONS = [
    ('plumbing', 'Plumbing Repairs'),
    ('electrical', 'Electrical Repairs'),
    ('carpentry', 'Carpentry Work'),
    ('painting', 'Painting Services'),
    ('appliance', 'Appliance Repair'),
    ('hvac', 'HVAC Maintenance'),
    ('roof', 'Roof Repairs'),
    ('pest', 'Pest Control'),
    ('locksmith', 'Locksmith Services'),
]

GARDENING_OPTIONS = [
    ('lawn', 'Lawn Maintenance'),
    ('garden', 'Garden Design'),
    ('irrigation', 'Irrigation Systems'),
    ('tree', 'Tree Services'),
    ('landscaping', 'Landscaping'),
    ('planting', 'Plant Installation'),
    ('mulching', 'Mulching Services'),
    ('fertilization', 'Fertilization Services'),
    ('weed_control', 'Weed Control'),
]

AUTOMATION_OPTIONS = [
    ('lighting', 'Smart Lighting'),
    ('security', 'Security Systems'),
    ('climate', 'Climate Control'),
    ('entertainment', 'Home Entertainment'),
    ('voice', 'Voice Control Systems'),
    ('door_locks', 'Smart Door Locks'),
    ('cameras', 'Smart Cameras'),
    ('speakers', 'Smart Speakers'),
    ('appliances', 'Smart Appliances'),
]

SECURITY_OPTIONS = [
    ('cctv', 'CCTV Installation'),
    ('alarm', 'Alarm Systems'),
    ('access', 'Access Control'),
    ('monitoring', '24/7 Monitoring'),
    ('consultation', 'Security Consultation'),
    ('fire_safety', 'Fire Safety Systems'),
    ('intercom', 'Intercom Systems'),
    ('biometric', 'Biometric Security'),
    ('smart_locks', 'Smart Lock Installation'),
]

COOKING_OPTIONS = [
    ('veg', 'Vegetarian Dishes'),
    ('non_veg', 'Non-Vegetarian Dishes'),
]

# Area Coverage Choices
AREA_COVERAGE_CHOICES = [
    ('studio', 'Studio Apartment (300-500 sq ft)'),
    ('1bhk', '1 BHK (500-800 sq ft)'),
    ('2bhk', '2 BHK (800-1200 sq ft)'),
    ('3bhk', '3 BHK (1200-1800 sq ft)'),
    ('4bhk', '4 BHK (1800-2500 sq ft)'),
    ('villa', 'Villa (2500+ sq ft)'),
    ('commercial_small', 'Small Commercial (500-1000 sq ft)'),
    ('commercial_medium', 'Medium Commercial (1000-2000 sq ft)'),
    ('commercial_large', 'Large Commercial (2000+ sq ft)'),
]

# Property Type Choices
PROPERTY_TYPE_CHOICES = [
    ('residential', 'Residential'),
    ('commercial', 'Commercial'),
    ('industrial', 'Industrial'),
    ('mixed', 'Mixed Use'),
]

# Location Type Choices
LOCATION_TYPE_CHOICES = [
    ('urban', 'Urban'),
    ('suburban', 'Suburban'),
    ('rural', 'Rural'),
]

VEG_DISH_TYPES = [
    ('chapati_curry', 'Chapati + Curry'),
    ('paratha', 'Paratha'),
]

class User(models.Model):
    name     = models.CharField(max_length=100)
    email    = models.EmailField(unique=True)
    phone    = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    address  = models.TextField()

    def __str__(self):
        return self.name


class ServiceProvider(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.EmailField(unique=True)
    phone        = models.CharField(max_length=15)
    password     = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100, choices=SERVICE_TYPE_CHOICES)
    location     = models.CharField(max_length=100)
    rating       = models.FloatField(default=0)
    
    # Service-specific fields
    cleaning_option = models.CharField(max_length=20, choices=CLEANING_OPTIONS, null=True, blank=True)
    maintenance_option = models.CharField(max_length=20, choices=MAINTENANCE_OPTIONS, null=True, blank=True)
    gardening_option = models.CharField(max_length=20, choices=GARDENING_OPTIONS, null=True, blank=True)
    automation_option = models.CharField(max_length=20, choices=AUTOMATION_OPTIONS, null=True, blank=True)
    security_option = models.CharField(max_length=20, choices=SECURITY_OPTIONS, null=True, blank=True)
    
    # Additional provider details
    experience_years = models.IntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    availability = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    languages = models.CharField(max_length=200, blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    service_areas = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"


class Service(models.Model):
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Service-specific fields
    cleaning_option = models.CharField(max_length=20, choices=CLEANING_OPTIONS, null=True, blank=True)
    maintenance_option = models.CharField(max_length=20, choices=MAINTENANCE_OPTIONS, null=True, blank=True)
    gardening_option = models.CharField(max_length=20, choices=GARDENING_OPTIONS, null=True, blank=True)
    automation_option = models.CharField(max_length=20, choices=AUTOMATION_OPTIONS, null=True, blank=True)
    security_option = models.CharField(max_length=20, choices=SECURITY_OPTIONS, null=True, blank=True)
    cooking_option = models.CharField(max_length=20, choices=COOKING_OPTIONS, null=True, blank=True)
    
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    area_coverage = models.CharField(max_length=100, choices=AREA_COVERAGE_CHOICES, null=True, blank=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, null=True, blank=True)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES, null=True, blank=True)
    square_footage = models.IntegerField(null=True, blank=True, help_text="Exact square footage of the property")
    floor_count = models.IntegerField(null=True, blank=True, help_text="Number of floors in the property")
    includes = models.TextField(null=True, blank=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"


class MenuItem(models.Model):
    COOKING_TYPE_CHOICES = [
        ('veg', 'Veg'),
        ('nonveg', 'Non-Veg'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cooking_type = models.CharField(max_length=10, choices=COOKING_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.cooking_type})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateField(null=True, blank=True)
    booking_time = models.TimeField(null=True, blank=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # Cooking service specific fields
    dish = models.ForeignKey('VegDish', on_delete=models.SET_NULL, null=True, blank=True, related_name='booked_as_dish')
    non_veg_dish = models.ForeignKey('NonVegDish', on_delete=models.SET_NULL, null=True, blank=True, related_name='booked_as_non_veg_dish')
    dish_type = models.CharField(max_length=10, choices=[('veg', 'Vegetarian'), ('non_veg', 'Non-Vegetarian')], null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    special_instructions = models.TextField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    menu_items = models.ManyToManyField(MenuItem, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        provider_name = self.provider.name if self.provider else "No Provider"
        return f"Booking {self.id} – {self.user.name} with {provider_name}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount  = models.DecimalField(max_digits=10, decimal_places=2)
    mode    = models.CharField(max_length=50)
    status  = models.CharField(max_length=20)

    def __str__(self):
        return f"Payment {self.id} – {self.status}"


class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating  = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review {self.id} – {self.rating} stars"


class CookingService(models.Model):
    CATEGORY_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non_veg', 'Non-Vegetarian'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class VegDish(models.Model):
    name = models.CharField(max_length=100)
    dish_type = models.CharField(max_length=20, choices=VEG_DISH_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_dish_type_display()})"

class NonVegDish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Bread(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
