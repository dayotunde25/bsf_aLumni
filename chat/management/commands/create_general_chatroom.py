from django.core.management.base import BaseCommand
from django.db import transaction
from chat.models import ChatRoom
from users.models import User

class Command(BaseCommand):
    help = 'Creates a general chatroom and adds all users to it'

    def handle(self, *args, **options):
        self.stdout.write('Creating general chatroom...')
        try:
            with transaction.atomic():
                general_room, created = ChatRoom.objects.get_or_create(
                    name='General',
                    room_type='public'
                )
                if created:
                    self.stdout.write(self.style.SUCCESS('General chatroom created.'))
                else:
                    self.stdout.write(self.style.WARNING('General chatroom already exists.'))

                users = User.objects.all()
                general_room.participants.add(*users)
                self.stdout.write(self.style.SUCCESS(f'Added all {users.count()} users to the General chatroom.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
