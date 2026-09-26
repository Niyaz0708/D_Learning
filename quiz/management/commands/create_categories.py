from django.core.management.base import BaseCommand
from quiz.models import Category

class Command(BaseCommand):
    help = 'Creates initial categories for the quiz app'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Python Programming',
                'description': 'Test your knowledge of Python programming concepts, syntax, and best practices.',
                'icon': 'bi-code-slash'
            },
            {
                'name': 'Data Structures',
                'description': 'Challenge yourself with questions about arrays, linked lists, trees, and more.',
                'icon': 'bi-diagram-3'
            },
            {
                'name': 'Algorithms',
                'description': 'Practice solving problems related to sorting, searching, and algorithmic complexity.',
                'icon': 'bi-graph-up'
            },
            {
                'name': 'Web Development',
                'description': 'Learn about HTML, CSS, JavaScript, and modern web frameworks.',
                'icon': 'bi-globe'
            },
            {
                'name': 'Database Systems',
                'description': 'Test your knowledge of SQL, database design, and management systems.',
                'icon': 'bi-database'
            },
            {
                'name': 'Operating Systems',
                'description': 'Explore concepts related to process management, memory, and file systems.',
                'icon': 'bi-cpu'
            }
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'icon': category_data['icon']
                }
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created category "{category_data["name"]}"')
            ) 