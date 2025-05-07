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

def create_categories_and_blogs():
    print("Creating categories and blogs...")
    
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
    
    # Define categories with their sample blogs
    categories_data = {
        'Health & Fitness': {
            'slug': 'health-fitness',
            'description': 'Tips and advice for maintaining a healthy lifestyle',
            'blogs': [
                {
                    'title': 'The Benefits of High-Intensity Interval Training',
                    'content': '''High-Intensity Interval Training (HIIT) has become increasingly popular for its efficiency and effectiveness. This workout approach alternates between short bursts of intense exercise and recovery periods.

Research shows HIIT can burn more calories in less time, increase metabolism, improve heart health, and help build endurance without requiring specialized equipment or gym memberships.''',
                },
                {
                    'title': 'Nutrition Fundamentals: Building a Balanced Diet',
                    'content': '''Creating a balanced diet doesn't have to be complicated. The key is understanding the role of macronutrients (proteins, carbohydrates, and fats) and micronutrients (vitamins and minerals) in your overall health.

This article provides practical guidance on portion control, meal planning, and making sustainable dietary choices that support your health goals while still enjoying your favorite foods.''',
                },
                {
                    'title': 'Mind-Body Connection: Mental Health Benefits of Exercise',
                    'content': '''Regular physical activity doesn't just improve your physical health—it also has profound effects on your mental wellbeing. Exercise stimulates the release of endorphins, reduces stress hormones, and can improve sleep quality.

Studies show consistent exercise can be as effective as medication for treating mild to moderate depression and anxiety, while also building resilience against future mental health challenges.''',
                },
                {
                    'title': 'Recovery Strategies for Athletes and Fitness Enthusiasts',
                    'content': '''Proper recovery is as important as your workout itself. This comprehensive guide covers science-backed recovery methods including sleep optimization, nutrition timing, active recovery, compression therapy, and stress management techniques.

Learn how elite athletes structure their recovery protocols and how you can adapt these strategies to your own fitness routine for better performance and injury prevention.''',
                },
            ]
        },
        'Career': {
            'slug': 'career',
            'description': 'Career development, workplace skills, and professional growth',
            'blogs': [
                {
                    'title': 'Navigating Career Transitions: A Step-by-Step Guide',
                    'content': '''Changing careers can be daunting, but with proper planning, it can become an exciting opportunity for growth. This guide walks you through each phase of a successful transition, from self-assessment to skills transfer analysis and building a new professional network.

Learn how to identify transferable skills, bridge knowledge gaps, and position yourself effectively in a new industry or role while maintaining financial stability.''',
                },
                {
                    'title': 'Effective Negotiation Strategies for Workplace Success',
                    'content': '''Negotiation is an essential skill in any professional environment. This article covers preparation techniques, understanding leverage, creating value in negotiations, and handling objections gracefully.

Whether you're discussing salary, project resources, or team responsibilities, mastering these principles will help you achieve better outcomes while preserving important professional relationships.''',
                },
                {
                    'title': 'Building a Personal Brand in the Digital Age',
                    'content': '''Your personal brand is how others perceive you professionally. In today's digital landscape, strategically managing this perception is more important than ever. This practical guide covers optimizing your online presence, developing thought leadership, and creating consistency across platforms.

Learn how to showcase your expertise authentically while aligning your personal brand with your career objectives.''',
                },
                {
                    'title': 'Remote Work Productivity: Systems for Success',
                    'content': '''Working remotely offers flexibility but presents unique challenges for staying productive and engaged. This article provides evidence-based strategies for creating effective workflows, managing digital distractions, and maintaining work-life boundaries.

Discover how to design your workspace, implement time management techniques, and use technology thoughtfully to thrive in a remote or hybrid work environment.''',
                },
            ]
        },
        'Self-Improvement': {
            'slug': 'self-improvement',
            'description': 'Personal development, habits, and mindset',
            'blogs': [
                {
                    'title': 'The Science of Habit Formation and Change',
                    'content': '''Understanding the neurological basis of habits can dramatically improve your ability to create positive changes in your life. This article explores the habit loop of cue, routine, and reward, and how to use this knowledge to your advantage.

Learn practical techniques for breaking unwanted habits and establishing new ones that align with your goals, based on the latest research in behavioral psychology and neuroscience.''',
                },
                {
                    'title': 'Developing Emotional Intelligence for Better Relationships',
                    'content': '''Emotional intelligence—the ability to understand and manage your emotions while navigating social interactions effectively—can significantly impact your personal and professional relationships. This comprehensive guide covers the five components of emotional intelligence and how to strengthen each one.

Discover practical exercises for improving self-awareness, self-regulation, motivation, empathy, and social skills.''',
                },
                {
                    'title': 'Mindfulness Practices for Daily Life',
                    'content': '''Incorporating mindfulness into your daily routine doesn't require hours of meditation. This article presents accessible techniques for bringing present-moment awareness to everyday activities, from commuting to eating to workplace interactions.

Learn how these small shifts in attention can reduce stress, improve focus, and enhance overall wellbeing, with specific applications for busy lifestyles.''',
                },
                {
                    'title': 'Overcoming Procrastination: Psychological Insights and Strategies',
                    'content': '''Procrastination is rarely about laziness—it's often a complex emotional response to tasks that trigger anxiety, perfectionism, or overwhelm. This article examines the psychological mechanisms behind procrastination and offers evidence-based approaches to address the root causes.

Explore techniques like time-blocking, task decomposition, and implementation intentions that can help you move forward on important projects with less resistance.''',
                },
            ]
        },
        'Education': {
            'slug': 'education',
            'description': 'Learning strategies, educational resources, and academic success',
            'blogs': [
                {
                    'title': 'Effective Learning Techniques Based on Cognitive Science',
                    'content': '''Not all study methods are equally effective. This article examines learning techniques that have strong scientific support, including spaced repetition, retrieval practice, interleaving, and elaborative interrogation.

Understand why highlighting and re-reading are often inefficient, and how to implement more effective approaches to learn material more deeply in less time, whether you're a student or lifelong learner.''',
                },
                {
                    'title': 'The Future of Education: Emerging Trends and Technologies',
                    'content': '''Education is evolving rapidly with advances in technology and new understandings of how people learn. This article explores developments like adaptive learning systems, microlearning, immersive technologies, and competency-based education models.

Examine how these innovations are reshaping traditional educational structures and creating new opportunities for personalized, accessible learning across age groups and geographical boundaries.''',
                },
                {
                    'title': 'Critical Thinking in the Information Age',
                    'content': '''In an era of information abundance and misinformation, critical thinking skills are more essential than ever. This comprehensive guide covers frameworks for evaluating claims, recognizing cognitive biases, and constructing valid arguments.

Learn practical methods for distinguishing reliable sources, questioning assumptions, and making better decisions in academic contexts and everyday life.''',
                },
                {
                    'title': 'Continuous Learning: Strategies for Professional Development',
                    'content': '''Ongoing learning is crucial in today's rapidly changing work environment. This article outlines approaches for identifying learning needs, creating structured learning plans, and integrating new knowledge into your professional practice.

Discover how to leverage online courses, communities of practice, mentorship, and reflective learning to continuously expand your capabilities and remain adaptable throughout your career.''',
                },
            ]
        }
    }
    
    # Create categories and blogs
    with transaction.atomic():
        for category_name, category_data in categories_data.items():
            # Create or get category
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={
                    'slug': category_data['slug'],
                    'description': category_data['description']
                }
            )
            
            if created:
                print(f"Created category: {category_name}")
            else:
                print(f"Category '{category_name}' already exists")
            
            # Create blogs for this category
            for blog_data in category_data['blogs']:
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
                    blog.categories.add(category)
                    print(f"Created blog: {blog.title}")
                else:
                    print(f"Blog with title '{blog_data['title']}' already exists, skipping")

if __name__ == "__main__":
    create_categories_and_blogs()
    print("Done!") 