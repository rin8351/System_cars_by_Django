"""
Management command to load demo data into the database.

Usage:
    python manage.py load_demo_data
    python manage.py load_demo_data --clear  # Delete existing data first
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from carsdb.models import parts, cars, car_part


class Command(BaseCommand):
    help = 'Loads demo data into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing data before loading',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Deleting existing data...'))
            car_part.objects.all().delete()
            cars.objects.all().delete()
            parts.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data deleted'))

        self.stdout.write('Loading demo data...')

        with transaction.atomic():
            # Create parts
            parts_data = [
                # Engines
                {'type': 'Engine', 'price': 150000, 'model_p': 'V6 3.0L', 'count_p': 1, 'params': '250 hp'},
                {'type': 'Engine', 'price': 250000, 'model_p': 'V8 5.0L', 'count_p': 1, 'params': '450 hp'},
                {'type': 'Engine', 'price': 180000, 'model_p': 'Inline-4 2.0L Turbo', 'count_p': 1, 'params': '300 hp'},
                
                # Transmissions
                {'type': 'Transmission', 'price': 80000, 'model_p': '8-speed AT', 'count_p': 1, 'params': 'Automatic'},
                {'type': 'Transmission', 'price': 120000, 'model_p': 'DSG-7', 'count_p': 1, 'params': 'Dual-clutch'},
                {'type': 'Transmission', 'price': 60000, 'model_p': '6-speed MT', 'count_p': 1, 'params': 'Manual'},
                
                # Body
                {'type': 'Body', 'price': 200000, 'model_p': 'Full sedan', 'count_p': 1, 'params': 'Steel'},
                {'type': 'Body', 'price': 280000, 'model_p': 'Full SUV', 'count_p': 1, 'params': 'Aluminum'},
                {'type': 'Body', 'price': 220000, 'model_p': 'Sport coupe', 'count_p': 1, 'params': 'Carbon fiber'},
                
                # Wheels
                {'type': 'Wheels', 'price': 15000, 'model_p': 'R17 standard', 'count_p': 4, 'params': '205/55'},
                {'type': 'Wheels', 'price': 25000, 'model_p': 'R19 sport', 'count_p': 4, 'params': '245/40'},
                {'type': 'Wheels', 'price': 35000, 'model_p': 'R21 premium', 'count_p': 4, 'params': '275/35'},
                
                # Interior
                {'type': 'Interior', 'price': 50000, 'model_p': 'Basic fabric', 'count_p': 1, 'params': 'Fabric'},
                {'type': 'Interior', 'price': 120000, 'model_p': 'Premium leather', 'count_p': 1, 'params': 'Genuine leather'},
                {'type': 'Interior', 'price': 80000, 'model_p': 'Comfort eco-leather', 'count_p': 1, 'params': 'Eco-leather'},
                
                # Electronics
                {'type': 'Electronics', 'price': 30000, 'model_p': 'Basic system', 'count_p': 1, 'params': 'ABS, ESP'},
                {'type': 'Electronics', 'price': 80000, 'model_p': 'Premium multimedia', 'count_p': 1, 'params': '10" screen, navigation'},
                {'type': 'Electronics', 'price': 150000, 'model_p': 'Autopilot Level 2', 'count_p': 1, 'params': 'Adaptive cruise'},
                
                # Other
                {'type': 'Suspension', 'price': 70000, 'model_p': 'Independent multi-link', 'count_p': 1, 'params': 'Adaptive'},
                {'type': 'Suspension', 'price': 45000, 'model_p': 'MacPherson standard', 'count_p': 1, 'params': 'Basic'},
                {'type': 'Brakes', 'price': 40000, 'model_p': 'Vented discs', 'count_p': 1, 'params': '350mm'},
            ]

            created_parts = []
            for part_data in parts_data:
                part = parts.objects.create(**part_data)
                created_parts.append(part)
            
            self.stdout.write(self.style.SUCCESS(f'Created {len(created_parts)} parts'))

            # Create cars
            cars_data = [
                {
                    'name': 'Standard Sedan',
                    'margin': 15,
                    'parts_indices': [2, 5, 6, 9, 12, 15, 19, 20]  # Economy trim
                },
                {
                    'name': 'Comfort Sedan',
                    'margin': 20,
                    'parts_indices': [0, 3, 6, 10, 14, 16, 18, 20]  # Mid trim
                },
                {
                    'name': 'Premium SUV',
                    'margin': 25,
                    'parts_indices': [1, 4, 7, 11, 13, 16, 17, 18, 20]  # Premium
                },
                {
                    'name': 'Sport Coupe',
                    'margin': 30,
                    'parts_indices': [1, 4, 8, 10, 13, 16, 17, 18, 20]  # Sport
                },
                {
                    'name': 'Economy Compact',
                    'margin': 10,
                    'parts_indices': [2, 5, 6, 9, 12, 15, 19, 20]  # Minimal
                },
            ]

            for car_data in cars_data:
                parts_indices = car_data.pop('parts_indices')
                car = cars.objects.create(
                    name=car_data['name'],
                    margin=car_data['margin']
                )
                
                # Add parts to the car
                for idx in parts_indices:
                    if idx < len(created_parts):
                        part = created_parts[idx]
                        car.parts.add(part)
                        # Create car_part link
                        car_part.objects.create(
                            car=car,
                            part=part,
                            name=car.name
                        )
                
                # Save car to recalculate price
                car.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created car: {car.name} '
                        f'(price: ${car.price:,}, margin: {car.margin}%)'
                    )
                )

        self.stdout.write(self.style.SUCCESS('\nDemo data loaded successfully!'))
        self.stdout.write(self.style.WARNING('\nYou can now log in and browse the data'))
        self.stdout.write('Go to: http://127.0.0.1:8000/')
