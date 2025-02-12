import logging
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from crawler.celery import app as celery_app

from .models import CrawlResult
from .schema import CrawlTask

logger = logging.getLogger(__name__)


@celery_app.task(
    name="crawl_url",
    max_retries=3,
    default_retry_delay=5,
    retry_backoff=True,
    retry_backoff_max=60,
)
def crawl_url(crawl_task: dict):
    logger.info(f"Crawling URL: {crawl_task}")

    try:
        crawl_task = CrawlTask(**crawl_task)
        if crawl_task.max_depth <= 0:
            return

        response = requests.get(crawl_task.url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a"):
            url = link.get("href")
            if not url:
                continue
            is_relative = url.startswith("/")
            is_hash = url.startswith("#")
            if is_hash:
                continue
            if is_relative:
                parsed = urlparse(crawl_task.url)
                hostname_with_protocol = parsed.scheme + "://" + parsed.netloc
                url = f"{hostname_with_protocol}{url}"
            CrawlResult.objects.create(task_id=crawl_task.id, url=url)
            subtask = CrawlTask(
                id=crawl_task.id, url=url, max_depth=crawl_task.max_depth - 1
            )
            crawl_url.delay(subtask.model_dump())

        return {"task_id": str(crawl_task.id), "url": crawl_task.url}
    except Exception as e:
        logger.error(f"Error crawling URL: {e}")
        return {"error": str(e)}
