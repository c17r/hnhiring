from django.urls import path

from app import views


urlpatterns = (
    path(
        '',
        views.HomepageView.as_view(),
        name='app-homepage'
    ),
    path(
        'month/<int:month_id>',
        views.MonthView.as_view(),
        name='app-month'
    )
)
