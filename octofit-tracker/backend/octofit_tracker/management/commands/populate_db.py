from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, LeaderboardEntry
from django.utils import timezone
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self.stdout.write(self.style.WARNING('Deleting old data...'))
            Activity.objects.all().delete()
            Workout.objects.all().delete()
            LeaderboardEntry.objects.all().delete()
            Team.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            marvel = Team.objects.create(name='Marvel')
            dc = Team.objects.create(name='DC')

            users = [
                User.objects.create_user(username='ironman', email='ironman@marvel.com', password='password'),
                User.objects.create_user(username='captainamerica', email='cap@marvel.com', password='password'),
                User.objects.create_user(username='spiderman', email='spiderman@marvel.com', password='password'),
                User.objects.create_user(username='batman', email='batman@dc.com', password='password'),
                User.objects.create_user(username='superman', email='superman@dc.com', password='password'),
                User.objects.create_user(username='wonderwoman', email='wonderwoman@dc.com', password='password'),
            ]
            marvel.members.add(users[0], users[1], users[2])
            dc.members.add(users[3], users[4], users[5])

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            for user in users:
                Activity.objects.create(user=user, activity_type='Running', duration=30, date=timezone.now().date())
                Activity.objects.create(user=user, activity_type='Cycling', duration=45, date=timezone.now().date())

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            for user in users:
                Workout.objects.create(user=user, description='Pushups and Situps', date=timezone.now().date())
                Workout.objects.create(user=user, description='Cardio Blast', date=timezone.now().date())

            self.stdout.write(self.style.SUCCESS('Creating leaderboard entries...'))
            LeaderboardEntry.objects.create(user=users[0], points=100, team=marvel)
            LeaderboardEntry.objects.create(user=users[1], points=90, team=marvel)
            LeaderboardEntry.objects.create(user=users[2], points=80, team=marvel)
            LeaderboardEntry.objects.create(user=users[3], points=110, team=dc)
            LeaderboardEntry.objects.create(user=users[4], points=95, team=dc)
            LeaderboardEntry.objects.create(user=users[5], points=85, team=dc)

            self.stdout.write(self.style.SUCCESS('Database populated with test data!'))

        # Ensure unique index on email
        from django.conf import settings
        from pymongo import MongoClient
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]
        db.users.create_index([('email', 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Ensured unique index on user email.'))
