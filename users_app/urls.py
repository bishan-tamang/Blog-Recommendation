from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users_app'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # History URLs
    path('history/reading/', views.reading_history, name='reading_history'),
    path('history/search/', views.search_history, name='search_history'),
    
    # Bookmarks URL
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    
    # Notifications URLs
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
] 