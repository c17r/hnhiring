from django.conf.urls import patterns, url

from app.views import HomepageView, MonthView

urlpatterns = patterns('',
    url(
        r"^$",
        HomepageView.as_view(),
        name="app-homepage"
    ),
    url(
        r"^month/(?P<month_id>[0-9]+)$",
        MonthView.as_view(),
        name="app-month"
    )
)
