from django.contrib import admin
from .models import UserInterest, Recommendation

@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'interest_level', 'created_at', 'updated_at')
    list_filter = ('category', 'interest_level', 'created_at')
    search_fields = ('user__username', 'category__name')
    raw_id_fields = ('user', 'category')
    list_editable = ('interest_level',)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'score', 'reason', 'is_viewed', 'created_at')
    list_filter = ('is_viewed', 'created_at')
    search_fields = ('user__username', 'blog__title', 'reason')
    raw_id_fields = ('user', 'blog')
    list_editable = ('is_viewed',)
    ordering = ('-score', '-created_at')
