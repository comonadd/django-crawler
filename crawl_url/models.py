import uuid
from django.db import models


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class CrawlResult(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    url = models.TextField()
