from django.db import models
from django.conf import settings
from blog_app.models import Blog, Category

# Create your models here.

class UserInterest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interests')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='interested_users')
    interest_level = models.PositiveSmallIntegerField(default=1)  # Scale of 1-10
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'category')
    
    def __str__(self):
        return f'{self.user.username} is interested in {self.category.name}'


class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='recommended_to')
    score = models.FloatField()  # Recommendation score
    reason = models.CharField(max_length=255)  # Why this blog was recommended
    is_viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'blog')
        ordering = ['-score', '-created_at']
    
    def __str__(self):
        return f'Recommendation for {self.user.username}: {self.blog.title}'
