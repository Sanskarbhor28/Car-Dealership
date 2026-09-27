from django.contrib import admin
from .models import CarMake, CarModel, Dealer, Review

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'description')
    search_fields = ('name', 'country')
    inlines = [CarModelInline]

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year')
    list_filter = ('car_make', 'type', 'year')
    search_fields = ('name', 'car_make__name')

class DealerAdmin(admin.ModelAdmin):
    list_display = ('dealer_id', 'full_name', 'city', 'state', 'phone')
    list_filter = ('state', 'city')
    search_fields = ('full_name', 'city', 'state')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('dealer', 'name', 'rating', 'sentiment', 'purchase', 'created_at')
    list_filter = ('sentiment', 'purchase', 'rating', 'created_at')
    search_fields = ('name', 'review', 'dealer__full_name')

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Dealer, DealerAdmin)
admin.site.register(Review, ReviewAdmin)
