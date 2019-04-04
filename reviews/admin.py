from django.contrib import admin
from .models import Reviews

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    model = Reviews
    # readonly_fields  = ('user',)  
    # raw_id_fields = ('user',)  





