from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, View
from django.db.models import Count
from .models import UserInterest, Recommendation
from blog_app.models import Blog, Category
from users_app.models import ReadingHistory

class RecommendationListView(ListView):
    model = Recommendation
    template_name = 'recommendations_app/recommendation_list.html'
    context_object_name = 'recommendations'
    paginate_by = 10
    
    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user, is_viewed=False)


class UserInterestView(View):
    template_name = 'recommendations_app/user_interests.html'
    
    def get(self, request):
        categories = Category.objects.all()
        user_interests = {
            interest.category_id: interest.interest_level 
            for interest in UserInterest.objects.filter(user=request.user)
        }
        
        return render(request, self.template_name, {
            'categories': categories,
            'user_interests': user_interests
        })


@login_required
def update_interests(request):
    if request.method == 'POST':
        # Clear existing interests
        UserInterest.objects.filter(user=request.user).delete()
        
        # Create new interests
        for category_id, level in request.POST.items():
            if category_id.startswith('category_'):
                try:
                    category_id = int(category_id.split('_')[1])
                    level = int(level)
                    if 1 <= level <= 10:
                        category = Category.objects.get(id=category_id)
                        UserInterest.objects.create(
                            user=request.user,
                            category=category,
                            interest_level=level
                        )
                except (ValueError, Category.DoesNotExist):
                    continue
        
        messages.success(request, 'Your interests have been updated.')
        return redirect('recommendations_app:user_interests')
    
    return redirect('recommendations_app:user_interests')


@login_required
def mark_recommendation_viewed(request, recommendation_id):
    recommendation = get_object_or_404(Recommendation, id=recommendation_id, user=request.user)
    recommendation.is_viewed = True
    recommendation.save()
    return redirect('blog_app:blog_detail', slug=recommendation.blog.slug)


@login_required
def refresh_recommendations(request):
    user = request.user
    
    # Get user's reading history
    read_blogs = ReadingHistory.objects.filter(user=user).values_list('blog', flat=True)
    
    # Get user's interests
    user_interests = UserInterest.objects.filter(user=user)
    
    # Get blogs the user hasn't read yet
    unread_blogs = Blog.objects.exclude(id__in=read_blogs)
    
    # Calculate recommendations based on user interests and blog categories
    recommendations = []
    for blog in unread_blogs:
        score = 0
        matching_categories = []
        
        # Calculate score based on matching categories and interest levels
        for interest in user_interests:
            if interest.category in blog.categories.all():
                score += interest.interest_level
                matching_categories.append(interest.category.name)
        
        if score > 0:
            reason = f"Matches your interests in: {', '.join(matching_categories)}"
            recommendations.append({
                'blog': blog,
                'score': score,
                'reason': reason
            })
    
    # Sort recommendations by score
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    # Create or update recommendations
    Recommendation.objects.filter(user=user).delete()
    for rec in recommendations[:10]:  # Keep top 10 recommendations
        Recommendation.objects.create(
            user=user,
            blog=rec['blog'],
            score=rec['score'],
            reason=rec['reason']
        )
    
    messages.success(request, 'Recommendations have been refreshed.')
    return redirect('recommendations_app:recommendation_list')
