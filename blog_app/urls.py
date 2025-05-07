from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    # Blog list and detail views
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Blog interaction endpoints
    path('blog/<int:blog_id>/like/', views.like_blog, name='like_blog'),
    path('blog/<int:blog_id>/bookmark/', views.bookmark_blog, name='bookmark_blog'),
    path('blog/<int:blog_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # Search and filter
    path('search/', views.search_blogs, name='search_blogs'),
    path('filter/', views.filter_blogs, name='filter_blogs'),
    path('blogs/search/', views.ajax_search, name='ajax_search'),
    
    # Category list
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
] 