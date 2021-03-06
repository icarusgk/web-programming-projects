from django.contrib import admin
from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "creator", "is_active")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "date_joined")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "time")

# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(User, UserAdmin)

