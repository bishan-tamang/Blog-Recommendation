from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, ReadingHistory, SearchHistory, Notification

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'read_at')
    list_filter = ('read_at',)
    search_fields = ('user__username', 'blog__title')
    raw_id_fields = ('user', 'blog')
    date_hierarchy = 'read_at'


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'searched_at')
    list_filter = ('searched_at',)
    search_fields = ('user__username', 'query')
    raw_id_fields = ('user',)
    date_hierarchy = 'searched_at'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'message', 'created_at', 'is_read')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')
    raw_id_fields = ('user', 'blog')
    date_hierarchy = 'created_at'
    list_editable = ('is_read',)
