from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model('quiz', 'Category')
    categories = [
        {
            'name': 'Python Programming',
            'description': 'Test your knowledge of Python programming concepts, syntax, and best practices.',
            'icon': 'bi-code-slash',
        },
        {
            'name': 'Data Structures',
            'description': 'Challenge yourself with questions about arrays, linked lists, trees, and more.',
            'icon': 'bi-diagram-3',
        },
        {
            'name': 'Algorithms',
            'description': 'Practice solving problems related to sorting, searching, and algorithmic complexity.',
            'icon': 'bi-graph-up',
        },
        {
            'name': 'Web Development',
            'description': 'Learn about HTML, CSS, JavaScript, and modern web frameworks.',
            'icon': 'bi-globe',
        },
        {
            'name': 'Database Systems',
            'description': 'Test your knowledge of SQL, database design, and management systems.',
            'icon': 'bi-database',
        },
        {
            'name': 'Operating Systems',
            'description': 'Explore concepts related to process management, memory, and file systems.',
            'icon': 'bi-cpu',
        },
    ]

    for category_data in categories:
        Category.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'description': category_data['description'],
                'icon': category_data['icon'],
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ('quiz', '0003_category_question_explanation_test_time_limit_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_code=migrations.RunPython.noop),
    ]
