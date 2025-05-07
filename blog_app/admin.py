from django.contrib import admin
from .models import Category, Blog

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published', 'views_count', 'get_like_count', 'get_comment_count')
    list_filter = ('is_published', 'created_at', 'categories')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    raw_id_fields = ('author',)
    filter_horizontal = ('categories',)
    
    def get_like_count(self, obj):
        return obj.likes.count()
    get_like_count.short_description = 'Likes'
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    get_comment_count.short_description = 'Comments'
