from django.contrib import admin
from .models import User, Category, Institution, Donation

admin.site.register(Category)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'quantity',
        'institution',
        'address',
        'zip_code',
        'city',
        'pick_up_date',
        'pick_up_time',
        'pick_up_comment',
        'phone_number',
        'user',
    )
