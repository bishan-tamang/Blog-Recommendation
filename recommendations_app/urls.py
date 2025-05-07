from django.urls import path
from . import views

app_name = 'recommendations_app'

urlpatterns = [
    # Recommendation views
    path('', views.RecommendationListView.as_view(), name='recommendation_list'),
    path('interests/', views.UserInterestView.as_view(), name='user_interests'),
    path('interests/update/', views.update_interests, name='update_interests'),
    
    # Mark recommendations as viewed
    path('mark-viewed/<int:recommendation_id>/', views.mark_recommendation_viewed, name='mark_viewed'),
    
    # Get new recommendations
    path('refresh/', views.refresh_recommendations, name='refresh_recommendations'),
] 