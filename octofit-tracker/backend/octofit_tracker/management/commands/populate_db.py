from django.core.management.base import BaseCommand
from djongo import models
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'marvel'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'dc'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'dc'},
        ]
        teams = [
            {'name': 'marvel', 'members': ['ironman@marvel.com', 'cap@marvel.com']},
            {'name': 'dc', 'members': ['wonderwoman@dc.com', 'batman@dc.com']},
        ]
        activities = [
            {'user_email': 'ironman@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user_email': 'cap@marvel.com', 'activity': 'Cycling', 'duration': 45},
            {'user_email': 'wonderwoman@dc.com', 'activity': 'Swimming', 'duration': 60},
            {'user_email': 'batman@dc.com', 'activity': 'Martial Arts', 'duration': 50},
        ]
        leaderboard = [
            {'team': 'marvel', 'points': 150},
            {'team': 'dc', 'points': 140},
        ]
        workouts = [
            {'user_email': 'ironman@marvel.com', 'workout': 'Chest Day', 'suggestion': 'Bench Press'},
            {'user_email': 'wonderwoman@dc.com', 'workout': 'Leg Day', 'suggestion': 'Squats'},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
