import uuid

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from crawl_url.schema import CrawlTask
from crawl_url.settings import DEFAULT_MAX_DEPTH

from .models import CrawlResult, Task
from .tasks import crawl_url


class HomeView(View):
    def get(self, request):
        return render(request, "index.html")


class StartCrawlView(View):
    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        url = request.POST["url"]
        max_depth = request.POST.get("max_depth", DEFAULT_MAX_DEPTH)

        crawl_task = CrawlTask(id=str(uuid.uuid4()), url=url, max_depth=max_depth)
        task = Task.objects.create(id=crawl_task.id)
        crawl_url.apply_async((crawl_task.model_dump(),))

        return redirect(reverse("crawl_results", kwargs={"task_id": task.id}))


class CrawlResultsView(ListView):
    model = CrawlResult
    template_name = "crawl_results.html"
    context_object_name = "results"
    paginate_by = 30

    def get_queryset(self):
        task_id = self.kwargs.get("task_id")
        return CrawlResult.objects.filter(task_id=task_id).select_related("task")
