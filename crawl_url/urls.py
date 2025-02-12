from django.urls import path

from . import views

urlpatterns = [
    path("", views.StartCrawlView.as_view(), name="index"),
    path(
        "crawl-results/<str:task_id>",
        views.CrawlResultsView.as_view(),
        name="crawl_results",
    ),
]
