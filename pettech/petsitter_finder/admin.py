from django.contrib import admin
from .models import PetType, PetSitter

# Register your models here.
@admin.register(PetType)
class PetTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']


@admin.register(PetSitter)
class PetSitterAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'experience_years', 'hourly_rate_min', 'hourly_rate_max', 'is_available']
    list_filter = ['is_available', 'pet_types', 'location']
    search_fields = ['user__first_name', 'user__last_name', 'location']
    filter_horizontal = ['pet_types']