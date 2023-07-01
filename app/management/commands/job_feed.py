from django.core.management.base import BaseCommand

from app.management import algolia as api
from app.models import Month, Entry


class Command(BaseCommand):
    help = "Calls HackerNews Job Feed"

    def handle(self, *args, **options):
        total = 0
        existing = 0

        for job in api.process_job_feed():
            total += 1

            month_name = job['time'].strftime('%B %Y')
            m = Month.objects.get_or_create(month_name)

            e, c = Entry.objects.get_or_create(
                hn_id=job['id'],
                defaults={
                    'content': self.format_content(job),
                    'date': job['time'],
                    'month': m,
                }
            )
            if not c:
                existing += 1

        print(f'   Total: {total}')
        print(f'Existing: {existing}')

    def format_content(self, job: dict) -> str:
        rv = job['title']
        rv += ('<br/>' * 2)
        if 'url' in job:
            rv += '<a href="{0}">{0}</a>'.format(job['url'])
        else:
            rv += job['text']
        rv += ('<br/>' * 2)
        rv += '[Job Feed]'

        return rv
