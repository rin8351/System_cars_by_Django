"""
Management команда для загрузки демонстрационных данных в базу

Использование:
    python manage.py load_demo_data
    python manage.py load_demo_data --clear  # Удалить существующие данные
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from carsdb.models import parts, cars, car_part


class Command(BaseCommand):
    help = 'Загружает демонстрационные данные в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Удалить все существующие данные перед загрузкой',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Удаление существующих данных...'))
            car_part.objects.all().delete()
            cars.objects.all().delete()
            parts.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Данные удалены'))

        self.stdout.write('Загрузка демонстрационных данных...')

        with transaction.atomic():
            # Создаем запчасти
            parts_data = [
                # Двигатели
                {'type': 'Двигатель', 'price': 150000, 'model_p': 'V6 3.0L', 'count_p': 1, 'params': '250 л.с.'},
                {'type': 'Двигатель', 'price': 250000, 'model_p': 'V8 5.0L', 'count_p': 1, 'params': '450 л.с.'},
                {'type': 'Двигатель', 'price': 180000, 'model_p': 'Inline-4 2.0L Turbo', 'count_p': 1, 'params': '300 л.с.'},
                
                # Коробки передач
                {'type': 'Коробка передач', 'price': 80000, 'model_p': 'АКПП 8-ступ', 'count_p': 1, 'params': 'Автомат'},
                {'type': 'Коробка передач', 'price': 120000, 'model_p': 'Робот DSG-7', 'count_p': 1, 'params': 'Робот'},
                {'type': 'Коробка передач', 'price': 60000, 'model_p': 'МКПП 6-ступ', 'count_p': 1, 'params': 'Механика'},
                
                # Кузовные детали
                {'type': 'Кузов', 'price': 200000, 'model_p': 'Седан полный', 'count_p': 1, 'params': 'Сталь'},
                {'type': 'Кузов', 'price': 280000, 'model_p': 'SUV полный', 'count_p': 1, 'params': 'Алюминий'},
                {'type': 'Кузов', 'price': 220000, 'model_p': 'Купе спорт', 'count_p': 1, 'params': 'Углепластик'},
                
                # Колеса
                {'type': 'Колеса', 'price': 15000, 'model_p': 'R17 стандарт', 'count_p': 4, 'params': '205/55'},
                {'type': 'Колеса', 'price': 25000, 'model_p': 'R19 спорт', 'count_p': 4, 'params': '245/40'},
                {'type': 'Колеса', 'price': 35000, 'model_p': 'R21 премиум', 'count_p': 4, 'params': '275/35'},
                
                # Салон
                {'type': 'Салон', 'price': 50000, 'model_p': 'Тканевый базовый', 'count_p': 1, 'params': 'Ткань'},
                {'type': 'Салон', 'price': 120000, 'model_p': 'Кожаный премиум', 'count_p': 1, 'params': 'Натур. кожа'},
                {'type': 'Салон', 'price': 80000, 'model_p': 'Эко-кожа комфорт', 'count_p': 1, 'params': 'Эко-кожа'},
                
                # Электроника
                {'type': 'Электроника', 'price': 30000, 'model_p': 'Базовая система', 'count_p': 1, 'params': 'ABS, ESP'},
                {'type': 'Электроника', 'price': 80000, 'model_p': 'Мультимедиа премиум', 'count_p': 1, 'params': '10" экран, навигация'},
                {'type': 'Электроника', 'price': 150000, 'model_p': 'Автопилот Level 2', 'count_p': 1, 'params': 'Адаптивный круиз'},
                
                # Дополнительно
                {'type': 'Подвеска', 'price': 70000, 'model_p': 'Независимая многорычажная', 'count_p': 1, 'params': 'Адаптивная'},
                {'type': 'Подвеска', 'price': 45000, 'model_p': 'МакФерсон стандарт', 'count_p': 1, 'params': 'Базовая'},
                {'type': 'Тормоза', 'price': 40000, 'model_p': 'Дисковые вентилируемые', 'count_p': 1, 'params': '350мм'},
            ]

            created_parts = []
            for part_data in parts_data:
                part = parts.objects.create(**part_data)
                created_parts.append(part)
            
            self.stdout.write(self.style.SUCCESS(f'✓ Создано {len(created_parts)} запчастей'))

            # Создаем автомобили
            cars_data = [
                {
                    'name': 'Седан Стандарт',
                    'margin': 15,
                    'parts_indices': [2, 5, 6, 9, 12, 15, 19, 20]  # Экономичная комплектация
                },
                {
                    'name': 'Седан Комфорт',
                    'margin': 20,
                    'parts_indices': [0, 3, 6, 10, 14, 16, 18, 20]  # Средняя комплектация
                },
                {
                    'name': 'SUV Премиум',
                    'margin': 25,
                    'parts_indices': [1, 4, 7, 11, 13, 16, 17, 18, 20]  # Премиум
                },
                {
                    'name': 'Купе Спорт',
                    'margin': 30,
                    'parts_indices': [1, 4, 8, 10, 13, 16, 17, 18, 20]  # Спортивная
                },
                {
                    'name': 'Экономка Эконом',
                    'margin': 10,
                    'parts_indices': [2, 5, 6, 9, 12, 15, 19, 20]  # Минимальная
                },
            ]

            for car_data in cars_data:
                parts_indices = car_data.pop('parts_indices')
                car = cars.objects.create(
                    name=car_data['name'],
                    margin=car_data['margin']
                )
                
                # Добавляем запчасти к автомобилю
                for idx in parts_indices:
                    if idx < len(created_parts):
                        part = created_parts[idx]
                        car.parts.add(part)
                        # Создаем связь car_part
                        car_part.objects.create(
                            car=car,
                            part=part,
                            name=car.name
                        )
                
                # Сохраняем автомобиль для пересчета цены
                car.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Создан автомобиль: {car.name} '
                        f'(цена: {car.price:,} руб, маржа: {car.margin}%)'
                    )
                )

        self.stdout.write(self.style.SUCCESS('\n✅ Демонстрационные данные успешно загружены!'))
        self.stdout.write(self.style.WARNING('\nТеперь вы можете войти в систему и просмотреть данные'))
        self.stdout.write('Перейдите по адресу: http://127.0.0.1:8000/')

