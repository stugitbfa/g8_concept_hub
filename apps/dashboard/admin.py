from django.contrib import admin
from .models import user
# Register your models here.

class userAdmin(admin.ModelAdmin):
    list_display = ['cid', 'email', 'mobile', 'is_active']
    list_filter = ['is_active']
    list_editable = ['mobile', 'is_active']
    search_fields = ['mobile', 'email']

    list_per_page = 50
admin.site.register(user, userAdmin)