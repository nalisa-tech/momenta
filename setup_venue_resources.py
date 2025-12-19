#!/usr/bin/env python
"""
🏢 Venue & Resource Management Setup Script
Creates sample venues and resources for the event management system
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
django.setup()

from events.models import Venue, Resource
from decimal import Decimal

def create_sample_venues():
    """Create sample venues for events"""
    venues_data = [
        {
            'name': 'Heroes Stadium',
            'address': 'Independence Avenue, Lusaka, Zambia',
            'capacity': 60000,
            'contact_person': 'Stadium Manager',
            'contact_phone': '+260 211 123456',
            'contact_email': 'manager@heroesstadium.zm',
            'hourly_rate': Decimal('2500.00'),
            'facilities': 'Large parking area, Professional sound system, Floodlights, VIP sections, Security, Medical facilities, Catering areas',
            'is_available': True
        },
        {
            'name': 'Mulungushi International Conference Centre',
            'address': 'Mulungushi Road, Lusaka, Zambia',
            'capacity': 3000,
            'contact_person': 'Events Coordinator',
            'contact_phone': '+260 211 234567',
            'contact_email': 'events@micc.zm',
            'hourly_rate': Decimal('1200.00'),
            'facilities': 'Air conditioning, Built-in AV equipment, Parking, Catering kitchen, Multiple halls, WiFi',
            'is_available': True
        },
        {
            'name': 'Levy Mwanawasa Stadium',
            'address': 'Ndola, Copperbelt Province, Zambia',
            'capacity': 49800,
            'contact_person': 'Facility Manager',
            'contact_phone': '+260 212 345678',
            'contact_email': 'bookings@levystadium.zm',
            'hourly_rate': Decimal('2000.00'),
            'facilities': 'Modern facilities, Parking, Sound system, Floodlights, VIP areas, Security',
            'is_available': True
        },
        {
            'name': 'Lusaka Playhouse',
            'address': 'Cairo Road, Lusaka, Zambia',
            'capacity': 500,
            'contact_person': 'Theatre Manager',
            'contact_phone': '+260 211 456789',
            'contact_email': 'bookings@lusakaplayhouse.zm',
            'hourly_rate': Decimal('800.00'),
            'facilities': 'Stage lighting, Sound system, Dressing rooms, Box office, Air conditioning',
            'is_available': True
        },
        {
            'name': 'Garden Court Hotel Conference Centre',
            'address': 'Church Road, Lusaka, Zambia',
            'capacity': 200,
            'contact_person': 'Conference Manager',
            'contact_phone': '+260 211 567890',
            'contact_email': 'conferences@gardencourt.zm',
            'hourly_rate': Decimal('600.00'),
            'facilities': 'WiFi, Projectors, Air conditioning, Catering services, Parking, Business center',
            'is_available': True
        },
        {
            'name': 'Woodlands Stadium',
            'address': 'Woodlands, Lusaka, Zambia',
            'capacity': 4000,
            'contact_person': 'Sports Manager',
            'contact_phone': '+260 211 678901',
            'contact_email': 'bookings@woodlandsstadium.zm',
            'hourly_rate': Decimal('1000.00'),
            'facilities': 'Football pitch, Athletics track, Changing rooms, Parking, Basic sound system',
            'is_available': True
        }
    ]
    
    print("🏢 Creating sample venues...")
    created_count = 0
    
    for venue_data in venues_data:
        venue, created = Venue.objects.get_or_create(
            name=venue_data['name'],
            defaults=venue_data
        )
        if created:
            created_count += 1
            print(f"✅ Created venue: {venue.name}")
        else:
            print(f"⚠️  Venue already exists: {venue.name}")
    
    print(f"\n🎯 Created {created_count} new venues")
    return created_count

def create_sample_resources():
    """Create sample resources for events"""
    resources_data = [
        # Sound Equipment
        {
            'name': 'Professional PA System (Large)',
            'resource_type': 'sound',
            'description': 'High-quality PA system suitable for large venues (5000+ people). Includes speakers, amplifiers, mixing console, and microphones.',
            'cost_per_day': Decimal('1500.00'),
            'quantity_available': 3,
            'supplier_name': 'Zambia Sound Solutions',
            'supplier_phone': '+260 977 123456',
            'is_available': True
        },
        {
            'name': 'Standard PA System (Medium)',
            'resource_type': 'sound',
            'description': 'Standard PA system for medium venues (500-2000 people). Includes basic speakers, mixer, and microphones.',
            'cost_per_day': Decimal('800.00'),
            'quantity_available': 5,
            'supplier_name': 'Zambia Sound Solutions',
            'supplier_phone': '+260 977 123456',
            'is_available': True
        },
        {
            'name': 'Wireless Microphone Set',
            'resource_type': 'sound',
            'description': 'Set of 4 wireless microphones with receivers and charging station.',
            'cost_per_day': Decimal('300.00'),
            'quantity_available': 8,
            'supplier_name': 'Audio Pro Zambia',
            'supplier_phone': '+260 966 234567',
            'is_available': True
        },
        
        # Lighting Equipment
        {
            'name': 'Stage Lighting Package (Professional)',
            'resource_type': 'lighting',
            'description': 'Complete stage lighting setup with LED spots, wash lights, moving heads, and lighting console.',
            'cost_per_day': Decimal('2000.00'),
            'quantity_available': 2,
            'supplier_name': 'Lusaka Lighting Co.',
            'supplier_phone': '+260 955 345678',
            'is_available': True
        },
        {
            'name': 'Basic Event Lighting',
            'resource_type': 'lighting',
            'description': 'Basic lighting setup for small to medium events. Includes LED par cans and basic controller.',
            'cost_per_day': Decimal('600.00'),
            'quantity_available': 4,
            'supplier_name': 'Lusaka Lighting Co.',
            'supplier_phone': '+260 955 345678',
            'is_available': True
        },
        
        # Stage Equipment
        {
            'name': 'Portable Stage Platform (Large)',
            'resource_type': 'stage',
            'description': '12m x 8m portable stage platform with safety barriers and steps.',
            'cost_per_day': Decimal('1200.00'),
            'quantity_available': 2,
            'supplier_name': 'Stage Masters Zambia',
            'supplier_phone': '+260 944 456789',
            'is_available': True
        },
        {
            'name': 'Small Stage Platform',
            'resource_type': 'stage',
            'description': '6m x 4m portable stage platform suitable for small events.',
            'cost_per_day': Decimal('600.00'),
            'quantity_available': 4,
            'supplier_name': 'Stage Masters Zambia',
            'supplier_phone': '+260 944 456789',
            'is_available': True
        },
        
        # Seating
        {
            'name': 'Plastic Chairs (White)',
            'resource_type': 'seating',
            'description': 'White plastic chairs suitable for outdoor and indoor events. Sold per 100 chairs.',
            'cost_per_day': Decimal('200.00'),
            'quantity_available': 20,  # 20 sets of 100 chairs = 2000 chairs
            'supplier_name': 'Event Furniture Hire',
            'supplier_phone': '+260 933 567890',
            'is_available': True
        },
        {
            'name': 'VIP Chairs (Cushioned)',
            'resource_type': 'seating',
            'description': 'Comfortable cushioned chairs for VIP sections. Sold per 50 chairs.',
            'cost_per_day': Decimal('300.00'),
            'quantity_available': 10,  # 10 sets of 50 chairs = 500 VIP chairs
            'supplier_name': 'Event Furniture Hire',
            'supplier_phone': '+260 933 567890',
            'is_available': True
        },
        
        # Security
        {
            'name': 'Security Personnel (Team of 10)',
            'resource_type': 'security',
            'description': 'Professional security team of 10 trained personnel for event security.',
            'cost_per_day': Decimal('2500.00'),
            'quantity_available': 3,  # 3 teams available
            'supplier_name': 'Zambia Security Services',
            'supplier_phone': '+260 922 678901',
            'is_available': True
        },
        {
            'name': 'Metal Detectors & Barriers',
            'resource_type': 'security',
            'description': 'Metal detection equipment and crowd control barriers.',
            'cost_per_day': Decimal('800.00'),
            'quantity_available': 5,
            'supplier_name': 'Zambia Security Services',
            'supplier_phone': '+260 922 678901',
            'is_available': True
        },
        
        # Catering Equipment
        {
            'name': 'Mobile Kitchen Unit',
            'resource_type': 'catering',
            'description': 'Complete mobile kitchen with cooking equipment, refrigeration, and serving area.',
            'cost_per_day': Decimal('1800.00'),
            'quantity_available': 2,
            'supplier_name': 'Catering Solutions Zambia',
            'supplier_phone': '+260 911 789012',
            'is_available': True
        },
        {
            'name': 'Serving Equipment Set',
            'resource_type': 'catering',
            'description': 'Complete serving equipment including chafing dishes, serving utensils, and warming trays.',
            'cost_per_day': Decimal('500.00'),
            'quantity_available': 6,
            'supplier_name': 'Catering Solutions Zambia',
            'supplier_phone': '+260 911 789012',
            'is_available': True
        },
        
        # Transportation
        {
            'name': 'Event Bus (50 Seater)',
            'resource_type': 'transport',
            'description': 'Comfortable bus for transporting event attendees or staff.',
            'cost_per_day': Decimal('1200.00'),
            'quantity_available': 4,
            'supplier_name': 'Zambia Transport Services',
            'supplier_phone': '+260 900 890123',
            'is_available': True
        },
        {
            'name': 'Equipment Truck',
            'resource_type': 'transport',
            'description': 'Large truck for transporting event equipment and supplies.',
            'cost_per_day': Decimal('800.00'),
            'quantity_available': 3,
            'supplier_name': 'Zambia Transport Services',
            'supplier_phone': '+260 900 890123',
            'is_available': True
        }
    ]
    
    print("\n🔧 Creating sample resources...")
    created_count = 0
    
    for resource_data in resources_data:
        resource, created = Resource.objects.get_or_create(
            name=resource_data['name'],
            defaults=resource_data
        )
        if created:
            created_count += 1
            print(f"✅ Created resource: {resource.name}")
        else:
            print(f"⚠️  Resource already exists: {resource.name}")
    
    print(f"\n🎯 Created {created_count} new resources")
    return created_count

def main():
    """Main setup function"""
    print("🚀 Setting up Venue & Resource Management System")
    print("=" * 60)
    
    # Create venues
    venues_created = create_sample_venues()
    
    # Create resources
    resources_created = create_sample_resources()
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETE!")
    print(f"📊 Summary:")
    print(f"   • Venues created: {venues_created}")
    print(f"   • Resources created: {resources_created}")
    print(f"   • Total venues: {Venue.objects.count()}")
    print(f"   • Total resources: {Resource.objects.count()}")
    
    print("\n🎯 Next Steps:")
    print("1. Access admin panel: http://127.0.0.1:8000/admin/")
    print("2. Go to 'Venues' section to manage venues")
    print("3. Go to 'Resources' section to manage resources")
    print("4. Create venue bookings and resource allocations for events")
    
    print("\n🏢 Available Venues:")
    for venue in Venue.objects.all():
        print(f"   • {venue.name} (Capacity: {venue.capacity:,}, Rate: K{venue.hourly_rate}/hr)")
    
    print("\n🔧 Available Resource Types:")
    resource_types = Resource.objects.values_list('resource_type', flat=True).distinct()
    for resource_type in resource_types:
        count = Resource.objects.filter(resource_type=resource_type).count()
        print(f"   • {resource_type.title()}: {count} resources")

if __name__ == '__main__':
    main()