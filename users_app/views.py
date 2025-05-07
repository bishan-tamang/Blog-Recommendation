from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Profile, ReadingHistory, SearchHistory, Notification
from blog_app.models import Bookmark
from .forms import UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('users_app:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users_app/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users_app/profile.html', {
        'user': request.user,
        'profile': request.user.profile
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('users_app:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'users_app/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def reading_history(request):
    history = ReadingHistory.objects.filter(user=request.user).order_by('-read_at')
    paginator = Paginator(history, 10)
    page = request.GET.get('page')
    reading_history = paginator.get_page(page)
    
    return render(request, 'users_app/reading_history.html', {'reading_history': reading_history})


@login_required
def search_history(request):
    history = SearchHistory.objects.filter(user=request.user)
    paginator = Paginator(history, 10)
    page = request.GET.get('page')
    history = paginator.get_page(page)
    
    return render(request, 'users_app/search_history.html', {'history': history})


@login_required
def bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    paginator = Paginator(bookmarks, 10)
    page = request.GET.get('page')
    bookmarks = paginator.get_page(page)
    
    return render(request, 'users_app/bookmarks.html', {'bookmarks': bookmarks})


@login_required
def notifications(request):
    # Get all notifications for the user, ordered by created_at
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Set up pagination
    paginator = Paginator(notifications, 10)  # 10 notifications per page
    page = request.GET.get('page')
    notifications = paginator.get_page(page)
    
    # Mark displayed notifications as read
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False,
        id__in=[n.id for n in notifications]
    )
    unread_notifications.update(is_read=True)
    
    return render(request, 'users_app/notifications.html', {'notifications': notifications})


@login_required
def mark_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
    return redirect('users_app:notifications')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('blog_app:blog_list')
        else:
            # Check if user exists
            from django.contrib.auth.models import User
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Incorrect password. Please try again.')
            else:
                messages.error(request, 'User does not exist. Please check your username or register.')
            return render(request, 'users_app/login.html')
    
    return render(request, 'users_app/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('blog_app:blog_list')
