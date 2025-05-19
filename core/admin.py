from django.contrib import admin
from .models import User, ServiceProvider, Service, Booking, Payment, Review, CookingService, VegDish, NonVegDish, MenuItem, Bread

admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Bread)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'cooking_type')
    list_filter = ('cooking_type',)
    search_fields = ('name',)
    ordering = ('cooking_type', 'name')
    list_per_page = 50

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'location', 'rating', 'availability')
    list_filter = ('service_type', 'availability')
    search_fields = ('name', 'email', 'phone', 'location', 'description')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            ('Basic Information', {
                'fields': ('name', 'email', 'phone', 'password', 'service_type', 'location', 'rating')
            }),
            ('Service Details', {
                'fields': ('description', 'experience_years', 'hourly_rate', 'availability')
            }),
            ('Additional Information', {
                'fields': ('certifications', 'languages', 'working_hours', 'service_areas')
            }),
        )
        
        # Add service-specific fields based on service type
        if obj and obj.service_type:
            service_fields = {
                'cleaning': ('cleaning_option',),
                'maintenance': ('maintenance_option',),
                'gardening': ('gardening_option',),
                'automation': ('automation_option',),
                'security': ('security_option',),
            }
            if obj.service_type in service_fields:
                fieldsets += (
                    ('Service-Specific Details', {
                        'fields': service_fields[obj.service_type],
                        'description': 'Select the specific service option based on the service type'
                    }),
                )
        
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.service_type:
            # Hide all service-specific fields except the one matching the service type
            service_fields = {
                'cleaning': ['maintenance_option', 'gardening_option', 'automation_option', 'security_option'],
                'maintenance': ['cleaning_option', 'gardening_option', 'automation_option', 'security_option'],
                'gardening': ['cleaning_option', 'maintenance_option', 'automation_option', 'security_option'],
                'automation': ['cleaning_option', 'maintenance_option', 'gardening_option', 'security_option'],
                'security': ['cleaning_option', 'maintenance_option', 'gardening_option', 'automation_option'],
            }
            if obj.service_type in service_fields:
                for field in service_fields[obj.service_type]:
                    if field in form.base_fields:
                        form.base_fields[field].widget = form.base_fields[field].hidden_widget()
        return form

    class Media:
        js = ('admin/js/service_admin.js',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'base_price', 'duration_hours')
    list_filter = ('service_type',)
    search_fields = ('name', 'description', 'includes')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            ('Basic Information', {
                'fields': ('name', 'service_type', 'description', 'base_price')
            }),
            ('Additional Information', {
                'fields': ('duration_hours', 'area_coverage', 'includes', 'price_per_hour'),
            }),
        )
        
        # Add service-specific fields based on service type
        if obj and obj.service_type:
            service_fields = {
                'cleaning': ('cleaning_option',),
                'maintenance': ('maintenance_option',),
                'gardening': ('gardening_option',),
                'automation': ('automation_option',),
                'security': ('security_option',),
            }
            if obj.service_type in service_fields:
                fieldsets += (
                    ('Service-Specific Details', {
                        'fields': service_fields[obj.service_type],
                        'description': 'Select the specific service option based on the service type'
                    }),
                )
        
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.service_type:
            # Hide all service-specific fields except the one matching the service type
            service_fields = {
                'cleaning': ['maintenance_option', 'gardening_option', 'automation_option', 'security_option'],
                'maintenance': ['cleaning_option', 'gardening_option', 'automation_option', 'security_option'],
                'gardening': ['cleaning_option', 'maintenance_option', 'automation_option', 'security_option'],
                'automation': ['cleaning_option', 'maintenance_option', 'gardening_option', 'security_option'],
                'security': ['cleaning_option', 'maintenance_option', 'gardening_option', 'automation_option'],
            }
            if obj.service_type in service_fields:
                for field in service_fields[obj.service_type]:
                    if field in form.base_fields:
                        form.base_fields[field].widget = form.base_fields[field].hidden_widget()
        return form

    class Media:
        js = ('admin/js/service_admin.js',)
