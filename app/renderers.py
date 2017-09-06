from django.core.urlresolvers import reverse
from django_medusa.renderers import StaticSiteRenderer
from app.models import Month


class MonthRenderer(StaticSiteRenderer):
    def get_paths(self):

        paths = []

        items = Month.objects.order_by("-id")
        for item in items:
            paths.append(reverse("app-month", kwargs={"month_id": item.id}))

        return paths


renderers = [MonthRenderer, ]
