from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from app.models import Month, Entry


class HomepageView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        current = Month.objects.order_by("-id")[0]
        return reverse("app-month", kwargs={'month_id': current.id})


class MonthView(ListView):

    model = Entry

    def get_queryset(self):
        entries = super(MonthView, self).get_queryset()
        month_id = self.kwargs['month_id']
        month = Month.objects.filter(id=month_id)[0]
        return entries.filter(month=month).order_by("-date")

    def get_context_data(self, **kwargs):
        context = super(MonthView, self).get_context_data(**kwargs)
        context['months'] = Month.objects.all().order_by("-id")
        context['month_id'] = int(self.kwargs['month_id'])
        return context

    def get(self, request, *args, **kwargs):
        return super(MonthView, self).get(request, *args, **kwargs)
