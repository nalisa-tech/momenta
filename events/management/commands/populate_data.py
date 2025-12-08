from django.core.management.base import BaseCommand
from events.models import Category, Event
from datetime import date, time


class Command(BaseCommand):
    help = 'Populate database with sample events'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating categories...')
        
        # Create categories
        music, _ = Category.objects.get_or_create(name='Music & Concerts', defaults={'slug': 'music'})
        tech, _ = Category.objects.get_or_create(name='Tech & Innovation', defaults={'slug': 'tech'})
        food, _ = Category.objects.get_or_create(name='Food & Festivals', defaults={'slug': 'food'})
        business, _ = Category.objects.get_or_create(name='Business & Conferences', defaults={'slug': 'business'})
        
        self.stdout.write(self.style.SUCCESS('✓ Categories created'))
        
        # Create sample events
        events_data = [
            {
                'title': 'Zambia Music Festival 2025',
                'description': 'Join us for the biggest music festival in Zambia featuring top local and international artists. Experience amazing performances, food, and entertainment.',
                'date': date(2025, 12, 15),
                'time': time(18, 0),
                'location': 'Lusaka Showgrounds',
                'category': music,
                'vip_seats_left': 50,
                'gold_seats_left': 150,
                'standard_seats_left': 500,
            },
            {
                'title': 'Tech Summit Zambia 2025',
                'description': 'The premier technology conference bringing together innovators, developers, and entrepreneurs. Learn about AI, blockchain, and the future of tech in Africa.',
                'date': date(2025, 11, 30),
                'time': time(9, 0),
                'location': 'Mulungushi International Conference Centre',
                'category': tech,
                'vip_seats_left': 30,
                'gold_seats_left': 100,
                'standard_seats_left': 300,
            },
            {
                'title': 'Lusaka Food & Wine Festival',
                'description': 'Celebrate Zambian cuisine and international flavors. Enjoy cooking demonstrations, wine tastings, and live entertainment.',
                'date': date(2025, 12, 8),
                'time': time(12, 0),
                'location': 'Arcades Shopping Mall',
                'category': food,
                'vip_seats_left': 40,
                'gold_seats_left': 120,
                'standard_seats_left': 400,
            },
            {
                'title': 'Business Leaders Conference',
                'description': 'Network with top business leaders and learn strategies for growth in the African market. Featuring keynote speakers and panel discussions.',
                'date': date(2025, 12, 1),
                'time': time(8, 30),
                'location': 'Radisson Blu Hotel',
                'category': business,
                'vip_seats_left': 25,
                'gold_seats_left': 75,
                'standard_seats_left': 200,
            },
        ]
        
        self.stdout.write('Creating events...')
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults=event_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {event.title}'))
            else:
                self.stdout.write(f'  Already exists: {event.title}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Database populated successfully!'))
