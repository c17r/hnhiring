from django.core.management.base import BaseCommand

import app.management.hackernews as hackernews
from app.models import Month, Entry


class Command(BaseCommand):
    help = "Calls HackerNews to get latest data"

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', action='store', type=str, dest='users', default='whoishiring')
        parser.add_argument('-a', '--all', action='store_true', dest='refresh_all')

    def handle(self, *args, **options):
        users = options["users"].split(",")
        total = 0
        existing = 0

        e, t = self.handle_current(users)
        existing += e
        total += t

        if options["refresh_all"]:
            e, t = self.handle_all()
            existing += e
            total += t

        print("   Total: %d" % total)
        print("Existing: %d" % existing)

    def handle_current(self, users):
        total = 0
        existing = 0
        for user in users:
            print(f'Processing {user}...')
            months = hackernews.get_months(user)
            current = months[0]
            current_month = Month.objects.get_or_create(current[0], current[1])
            print(f'\tProcessing {current_month}...')
            e, t = self.process_entries_for_month(current_month)
            existing += e
            total += t

        return existing, total

    def handle_all(self):
        total = 0
        existing = 0
        months = Month.objects.all().order_by("-id")
        for month in months:
            e, t = self.process_entries_for_month(month)
            existing += e
            total += t

        return existing, total

    def process_entries_for_month(self, month):
        total = 0
        existing = 0
        for entry in hackernews.get_data(str(month.hn_id)):
            total += 1
            e, c = Entry.objects.get_or_create(
                hn_id=entry[0],
                defaults={
                    "month": month,
                    "content": entry[1],
                    "date": entry[2]
                }
            )
            if c is False:
                existing += 1
                e.content = entry[1]
                e.save()

        return existing, total
