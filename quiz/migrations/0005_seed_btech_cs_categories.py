from django.db import migrations


def seed_btech_cs_categories(apps, schema_editor):
    Category = apps.get_model('quiz', 'Category')
    categories = [
        {
            'name': 'Computer Fundamentals',
            'description': 'Understand computer components, data representation, and the basics of how computers work.',
            'icon': 'bi-pc-display',
        },
        {
            'name': 'C Programming',
            'description': 'Learn C syntax, pointers, memory, functions, and structured programming.',
            'icon': 'bi-code-square',
        },
        {
            'name': 'C++ Programming',
            'description': 'Explore C++ programming, classes, templates, and the standard library.',
            'icon': 'bi-braces',
        },
        {
            'name': 'Java Programming',
            'description': 'Practice Java syntax, collections, classes, and building applications.',
            'icon': 'bi-cup-hot',
        },
        {
            'name': 'Object-Oriented Programming',
            'description': 'Study classes, objects, inheritance, encapsulation, and polymorphism.',
            'icon': 'bi-boxes',
        },
        {
            'name': 'Computer Organization and Architecture',
            'description': 'Learn how processors, memory, instructions, and computer systems fit together.',
            'icon': 'bi-motherboard',
        },
        {
            'name': 'Digital Logic Design',
            'description': 'Explore logic gates, Boolean circuits, combinational logic, and sequential systems.',
            'icon': 'bi-cpu-fill',
        },
        {
            'name': 'Computer Networks',
            'description': 'Understand network layers, protocols, routing, and reliable communication.',
            'icon': 'bi-diagram-2',
        },
        {
            'name': 'Data Communication',
            'description': 'Study transmission media, communication protocols, and network fundamentals.',
            'icon': 'bi-ethernet',
        },
        {
            'name': 'Software Engineering',
            'description': 'Learn software development life cycles, requirements, design, and maintenance.',
            'icon': 'bi-kanban',
        },
        {
            'name': 'Software Testing and QA',
            'description': 'Practice test design, automation concepts, debugging, and software quality.',
            'icon': 'bi-check2-square',
        },
        {
            'name': 'Cybersecurity',
            'description': 'Explore secure computing, common threats, access control, and risk reduction.',
            'icon': 'bi-shield-lock',
        },
        {
            'name': 'Theory of Computation',
            'description': 'Study formal languages, automata, grammars, and models of computation.',
            'icon': 'bi-infinity',
        },
        {
            'name': 'Compiler Design',
            'description': 'Learn lexical analysis, parsing, semantic checks, and code generation.',
            'icon': 'bi-file-earmark-code',
        },
        {
            'name': 'Artificial Intelligence',
            'description': 'Discover search, knowledge representation, reasoning, and intelligent systems.',
            'icon': 'bi-robot',
        },
        {
            'name': 'Machine Learning',
            'description': 'Explore model training, supervised learning, evaluation, and practical ML concepts.',
            'icon': 'bi-bezier2',
        },
        {
            'name': 'Data Science',
            'description': 'Practice working with data, preparing datasets, analysis, and clear communication.',
            'icon': 'bi-bar-chart-line',
        },
        {
            'name': 'Cloud Computing',
            'description': 'Understand cloud services, deployment models, containers, and scalable systems.',
            'icon': 'bi-cloud',
        },
        {
            'name': 'Mobile App Development',
            'description': 'Learn mobile application structure, interfaces, app lifecycle, and development.',
            'icon': 'bi-phone',
        },
        {
            'name': 'Linux and Shell Programming',
            'description': 'Build confidence with Linux commands, shell scripts, permissions, and processes.',
            'icon': 'bi-terminal',
        },
        {
            'name': 'Internet of Things',
            'description': 'Explore connected devices, sensors, embedded systems, and IoT communication.',
            'icon': 'bi-broadcast',
        },
        {
            'name': 'Human-Computer Interaction',
            'description': 'Study usability, accessible interfaces, user research, and interaction design.',
            'icon': 'bi-person-workspace',
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
        ('quiz', '0004_seed_default_categories'),
    ]

    operations = [
        migrations.RunPython(seed_btech_cs_categories, reverse_code=migrations.RunPython.noop),
    ]
