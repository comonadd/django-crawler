from pydantic import BaseModel


class CrawlTask(BaseModel):
    id: str
    url: str
    max_depth: int
