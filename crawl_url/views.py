import uuid

from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from crawl_url.settings import DEFAULT_MAX_DEPTH

from .models import CrawlResult, Task
from .schema import CrawlTask
from .tasks import crawl_url


def index(request):
    return render(request=request, template_name="index.html")


def start_crawl(request):
    if request.method == "POST":
        url = request.POST.get("url")
        max_depth = request.POST.get("max_depth", DEFAULT_MAX_DEPTH)
        crawl_task = CrawlTask(id=str(uuid.uuid4()), url=url, max_depth=max_depth)
        task = Task.objects.create(id=crawl_task.id)
        crawl_url.apply_async((crawl_task.model_dump(),))
        return redirect("crawl_results", task_id=task.id)

    return render(request=request, template_name="index.html")


def crawl_results(request, task_id):
    task_results = CrawlResult.objects.filter(task_id=task_id)
    paginator = Paginator(task_results, 10)
    page_number = request.GET.get("page")
    results = paginator.get_page(page_number)
    return render(
        request=request,
        template_name="crawl_results.html",
        context={"results": results},
    )
