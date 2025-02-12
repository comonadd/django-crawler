from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("crawl-results/<str:task_id>", views.crawl_results, name="crawl_results"),
    path("start-crawl", views.start_crawl, name="start_crawl"),
]
