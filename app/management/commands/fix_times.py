from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import app.management.hackernews as hackernews
from app.models import Month, Entry


class Command(BaseCommand):
    help = "Fixes the datetime for entries for a specified month"

    option_list = BaseCommand.option_list + (
        make_option(
            "--month",
            action="store",
            type=int,
            dest="month",
            default=0
        ),
    )

    def handle(self, *args, **options):
        month = None
        if options["month"] == 0:
            month = Month.objects.order_by("-id")[0]
        else:
            month = Month.objects.get(id=options["month"])

        for entry in Entry.objects.filter(month=month):
            dt = hackernews.get_entry_datetime(entry.hn_id)
            Entry.objects.filter(id=entry.id).update(date=dt)
