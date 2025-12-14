
from django.contrib import admin
from .models import SDGProject, Donation

# Register the models to make them visible in the admin interface
@admin.register(SDGProject)
class SDGProjectAdmin(admin.ModelAdmin):
    # List display columns for easy viewing of project data
    list_display = ('title', 'sdg_goal', 'target_amount', 'current_amount', 'creator', 'percentage_funded')
    # Add a filter sidebar to quickly find projects by Goal
    list_filter = ('sdg_goal', 'creator')
    # Search bar functionality
    search_fields = ('title', 'description')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('project', 'amount', 'phone_number', 'timestamp', 'user')
    list_filter = ('project', 'timestamp')
    date_hierarchy = 'timestamp' # Allows drilling down into date-based records