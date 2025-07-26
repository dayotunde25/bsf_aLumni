from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = 'Create admin user for Baptist Student Fellowship'

    def handle(self, *args, **options):
        try:
            admin_user = User.objects.create_user(
                username='bsf_admin',
                email='admin@baptiststudentfellowship.org',
                password='BSF@Admin2024!',
                first_name='BSF',
                last_name='Administrator',
                role='admin',
                is_staff=True,
                is_superuser=True
            )
            
            # Set birthday for demo
            admin_user.birthday_month = 1
            admin_user.birthday_day = 1
            admin_user.bio = 'System Administrator for Baptist Student Fellowship Alumni Management System'
            admin_user.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created admin user:\n'
                    f'Username: bsf_admin\n'
                    f'Email: admin@baptiststudentfellowship.org\n'
                    f'Password: BSF@Admin2024!\n'
                    f'Role: admin\n'
                    f'Please change the password after first login!'
                )
            )
            
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING('Admin user already exists!')
            )
