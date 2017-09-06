from django.conf.urls import url

from app import views


urlpatterns = [
    url(
        r"^$",
        views.HomepageView.as_view(),
        name="app-homepage"
    ),
    url(
        r"^month/(?P<month_id>[0-9]+)$",
        views.MonthView.as_view(),
        name="app-month"
    )
]
