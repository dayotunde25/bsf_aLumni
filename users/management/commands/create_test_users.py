import random
from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import User, ExecutiveRole, WorkerUnit, Post, Level

class Command(BaseCommand):
    help = 'Creates 30 sample users with profiles'

    def handle(self, *args, **options):
        self.stdout.write('Creating 30 sample users...')
        try:
            with transaction.atomic():
                for i in range(30):
                    first_name = f'User{i+1}'
                    last_name = 'Test'
                    username = f'testuser{i+1}'
                    email = f'testuser{i+1}@example.com'
                    password = 'password'
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                        phone=f'123456789{i:02}',
                        bio=f'This is the bio for {first_name} {last_name}.',
                        address=f'{i+1} Test Street, Test City',
                        birthday_day=random.randint(1, 28),
                        birthday_month=random.randint(1, 12),
                    )

                    # Add some roles and units
                    if i % 3 == 0:
                        ExecutiveRole.objects.create(
                            user=user,
                            position=random.choice(ExecutiveRole.EXECUTIVE_CHOICES)[0],
                            session='2022/2023',
                            start_year=2022,
                            end_year=2023
                        )
                    if i % 4 == 0:
                        WorkerUnit.objects.create(
                            user=user,
                            unit_name=random.choice(WorkerUnit.UNIT_CHOICES)[0],
                            session='2022/2023',
                            start_year=2022,
                            end_year=2023
                        )
                    if i % 5 == 0:
                        Post.objects.create(
                            user=user,
                            post_name=random.choice(Post.POST_CHOICES)[0],
                            session='2021/2022',
                            start_year=2021,
                            end_year=2022
                        )
                    if i % 2 == 0:
                        Level.objects.create(
                            user=user,
                            level_name=random.choice(Level.LEVEL_CHOICES)[0],
                            session='2020/2021',
                            start_year=2020,
                            end_year=2021
                        )

                    self.stdout.write(f'Successfully created user {username}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))

        self.stdout.write(self.style.SUCCESS('Finished creating sample users.'))
