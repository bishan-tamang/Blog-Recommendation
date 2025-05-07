import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_recommendation.settings')
django.setup()

from django.contrib.auth import get_user_model
from blog_app.models import Category, Blog
from django.utils.text import slugify
from django.db import transaction

User = get_user_model()

def create_sports_category_and_blogs():
    print("Creating Sports category and blogs...")
    
    # Get or create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Admin user created")
    
    # Create Sports category if it doesn't exist
    sports_category, created = Category.objects.get_or_create(
        name='Sports',
        defaults={
            'slug': 'sports',
            'description': 'Latest sports news and updates from around the world'
        }
    )
    
    if created:
        print("Sports category created")
    else:
        print("Sports category already exists")
    
    # Sample sports blog posts
    sample_blogs = [
        {
            'title': 'The Evolution of Football Tactics',
            'content': '''Football tactics have evolved significantly over the decades. From the early W-M formation to the modern pressing systems, coaches have continuously innovated to gain competitive advantages.

This article explores how tactical approaches have changed, influenced by technology, athleticism, and cultural factors. We look at how defensive solidity, possession-based play, and counter-attacking strategies have shaped the modern game.''',
        },
        {
            'title': 'Rising Stars in Tennis: Next Generation',
            'content': '''As the era of tennis legends gradually comes to an end, a new generation of talented players is emerging on both the ATP and WTA tours.

These young athletes bring fresh playing styles, extraordinary physical abilities, and a modern approach to the game. This article profiles the most promising talents under 23 and analyzes their potential to dominate the sport in the coming decade.''',
        },
        {
            'title': 'The Science Behind Marathon Training',
            'content': '''Marathon running requires more than just physical endurance. Modern training approaches combine physiological science, nutrition, psychology, and carefully structured programs.

This article examines evidence-based training methods, including heart rate zone training, periodization, recovery techniques, and nutritional strategies that help runners achieve their best performance while minimizing injury risks.''',
        },
        {
            'title': 'How Analytics is Changing Basketball',
            'content': '''Analytics has revolutionized basketball strategy at all levels of the game. Teams now employ data scientists and use advanced metrics to optimize player rotations, shot selection, and defensive schemes.

This article explores how data-driven decision making has changed player evaluation, in-game strategy, and even how players develop their skills to match what the numbers say is most valuable.''',
        },
    ]
    
    with transaction.atomic():
        for blog_data in sample_blogs:
            # Create a unique slug from the title
            slug = slugify(blog_data['title'])
            
            # Check if blog with this slug already exists
            if not Blog.objects.filter(slug=slug).exists():
                blog = Blog.objects.create(
                    title=blog_data['title'],
                    slug=slug,
                    author=admin_user,
                    content=blog_data['content'],
                    is_published=True
                )
                blog.categories.add(sports_category)
                print(f"Created blog: {blog.title}")
            else:
                print(f"Blog with title '{blog_data['title']}' already exists, skipping")

if __name__ == "__main__":
    create_sports_category_and_blogs()
    print("Done!") 