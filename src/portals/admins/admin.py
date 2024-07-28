from django.contrib import admin
from src.portals.admins.models import (
    Blog, BlogTag, BlogCategory, Company, CallRequest, Filing, Subscriber
)

class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'posted_by', 'read_time', 'likes', 'views', 'is_active', 'created_on'
    ]
    fieldsets = (
        (None, {'fields': ('title', 'description', 'detailed_description')}),
        ('Media Section', {'fields': (
            'thumbnail', 'banner_image')}),
        ('Linked', {
            'fields': ('posted_by', 'tags', 'blog_category'),
        }),
        ('Statistics', {
            'fields': ('read_time', 'likes', 'views'),
        }),
        ('Misc', {'fields': ('is_active', 'slug')}),

    )
    search_fields = [
        'title', 'posted_by', 'blog_category', 'tags'
    ]
    list_filter = [
        'is_active', 'blog_category',
    ]


class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_active', 'created_on']


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created_on']


class FilingAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'phone', 'company', 'amount', 'stripe_payment_intent', 'is_paid', 'is_active', 'created_on'
    ]


class CallRequestAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'phone', 'call_status', 'is_active', 'created_on'
    ]


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogTag, BlogTagAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Filing, FilingAdmin)
admin.site.register(CallRequest, CallRequestAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
