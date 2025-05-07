from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Blog, Category, Comment, Like, Bookmark
from users_app.models import ReadingHistory

class BlogListView(ListView):
    model = Blog
    template_name = 'blog_app/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Blog.objects.filter(is_published=True)
        
        # Apply search if query exists
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(categories__name__icontains=search_query)
            ).distinct()
            
            # Save search history for authenticated users
            if self.request.user.is_authenticated:
                from users_app.models import SearchHistory
                SearchHistory.objects.create(user=self.request.user, query=search_query)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all()
        
        # Get Sports category and its blogs
        try:
            sports_category = Category.objects.get(name='Sports')
            context['sports_blogs'] = Blog.objects.filter(
                categories=sports_category, 
                is_published=True
            ).order_by('-created_at')[:2]
            context['sports_category'] = sports_category
        except Category.DoesNotExist:
            context['sports_blogs'] = []
            context['sports_category'] = None
        
        # Get Health & Fitness category and its blogs
        try:
            health_fitness_category = Category.objects.get(name='Health & Fitness')
            context['health_fitness_blogs'] = Blog.objects.filter(
                categories=health_fitness_category, 
                is_published=True
            ).order_by('-created_at')[:2]
            context['health_fitness_category'] = health_fitness_category
        except Category.DoesNotExist:
            context['health_fitness_blogs'] = []
            context['health_fitness_category'] = None
        
        # Get Career category and its blogs
        try:
            career_category = Category.objects.get(name='Career')
            context['career_blogs'] = Blog.objects.filter(
                categories=career_category, 
                is_published=True
            ).order_by('-created_at')[:2]
            context['career_category'] = career_category
        except Category.DoesNotExist:
            context['career_blogs'] = []
            context['career_category'] = None
        
        # Get Self-Improvement category and its blogs
        try:
            self_improvement_category = Category.objects.get(name='Self-Improvement')
            context['self_improvement_blogs'] = Blog.objects.filter(
                categories=self_improvement_category, 
                is_published=True
            ).order_by('-created_at')[:2]
            context['self_improvement_category'] = self_improvement_category
        except Category.DoesNotExist:
            context['self_improvement_blogs'] = []
            context['self_improvement_category'] = None
        
        # Get Education category and its blogs
        try:
            education_category = Category.objects.get(name='Education')
            context['education_blogs'] = Blog.objects.filter(
                categories=education_category, 
                is_published=True
            ).order_by('-created_at')[:2]
            context['education_category'] = education_category
        except Category.DoesNotExist:
            context['education_blogs'] = []
            context['education_category'] = None
            
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_app/blog_detail.html'
    context_object_name = 'blog'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        
        # Increment view count
        blog.views_count += 1
        blog.save()
        
        # Add to reading history for authenticated users
        if self.request.user.is_authenticated:
            ReadingHistory.objects.get_or_create(user=self.request.user, blog=blog)
        
        # Get like and bookmark status
        if self.request.user.is_authenticated:
            context['is_liked'] = Like.objects.filter(user=self.request.user, blog=blog).exists()
            context['is_bookmarked'] = Bookmark.objects.filter(user=self.request.user, blog=blog).exists()
        
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'blog_app/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog_app/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['blogs'] = Blog.objects.filter(categories=category, is_published=True)
        return context


@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    like, created = Like.objects.get_or_create(user=request.user, blog=blog)
    
    if not created:
        like.delete()
        messages.success(request, 'Blog unliked successfully.')
    else:
        messages.success(request, 'Blog liked successfully.')
    
    return redirect('blog_app:blog_detail', slug=blog.slug)


@login_required
def bookmark_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, blog=blog)
    
    if not created:
        bookmark.delete()
        messages.success(request, 'Blog removed from bookmarks.')
    else:
        messages.success(request, 'Blog bookmarked successfully.')
    
    return redirect('blog_app:blog_detail', slug=blog.slug)


@login_required
def add_comment(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, id=blog_id)
        content = request.POST.get('content')
        
        if content:
            Comment.objects.create(user=request.user, blog=blog, content=content)
            messages.success(request, 'Comment added successfully.')
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    return redirect('blog_app:blog_detail', slug=blog.slug)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.user == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    else:
        messages.error(request, 'You are not authorized to delete this comment.')
    
    return redirect('blog_app:blog_detail', slug=comment.blog.slug)


def search_blogs(request):
    query = request.GET.get('q', '')
    blogs = Blog.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(categories__name__icontains=query),
        is_published=True
    ).distinct()
    
    # Save search history for authenticated users
    if request.user.is_authenticated and query:
        from users_app.models import SearchHistory
        SearchHistory.objects.create(user=request.user, query=query)
    
    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    
    return render(request, 'blog_app/search_results.html', {
        'blogs': blogs,
        'query': query
    })


def filter_blogs(request):
    category_id = request.GET.get('category')
    sort_by = request.GET.get('sort', '-created_at')
    
    blogs = Blog.objects.filter(is_published=True)
    
    if category_id and category_id.strip():
        try:
            category_id = int(category_id)
            blogs = blogs.filter(categories__id=category_id)
        except (ValueError, TypeError):
            pass  # Invalid category_id, ignore the filter
    
    # Apply sorting
    if sort_by == 'popular':
        blogs = blogs.order_by('-views_count', '-created_at')
    elif sort_by == 'most_liked':
        blogs = blogs.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
    else:
        blogs = blogs.order_by(sort_by)
    
    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    
    categories = Category.objects.all()
    
    return render(request, 'blog_app/filter_results.html', {
        'blogs': blogs,
        'categories': categories,
        'selected_category': category_id,
        'sort_by': sort_by
    })


def ajax_search(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'blogs': []})
        
    blogs = Blog.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(categories__name__icontains=query),
        is_published=True
    ).distinct()[:5]  # Limit to 5 results for the dropdown
    
    results = []
    for blog in blogs:
        results.append({
            'title': blog.title,
            'slug': blog.slug,
            'author': blog.author.username,
            'featured_image': blog.featured_image.url if blog.featured_image else None
        })
    
    return JsonResponse({'blogs': results})
