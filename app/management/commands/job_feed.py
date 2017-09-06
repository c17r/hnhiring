from django.core.management.base import BaseCommand

from app.management import hackernews
from app.models import Month, Entry


class Command(BaseCommand):
    help = "Calls HackerNews Job Feed"

    def handle(self, *args, **options):
        total = 0
        existing = 0

        for job in hackernews.process_job_feed():
            total += 1

            e, c = Entry.objects.get_or_create(
                hn_id=job['id'],
                defaults={
                    'content': job['title'] + '\n\n' + job['url'] if 'url' in job else job['text'],
                    'date': job['time_db'],
                    'month': Month.objects.get(name=job['time'].strftime('%B %Y')),
                }
            )
            if not c:
                existing += 1

        print(f'   Total: {total}')
        print(f'Existing: {existing}')
