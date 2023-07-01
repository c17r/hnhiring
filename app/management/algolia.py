import re
from datetime import datetime, timezone
from typing import Optional, List, Tuple, Iterator
import requests
from hackernews import HackerNews
from . import hackernews as old

_date_re = re.compile(r"(\w+ \d{4})")
hn = HackerNews()


def _get_date_from_item_title(item):
    return _date_re.findall(item.title)[0]


def get_months(user: Optional[str] = None, count: Optional[int] = 2) -> List[Tuple[str, str]]:
    user = "whoishiring" if user is None else user
    rv = []
    user = hn.user(user)
    for story_id in user.submitted:
        story = hn.item(story_id)
        if "hiring" in story.title:
            rv.append((_get_date_from_item_title(story), story.id))
            if len(rv) == count:
                break
    return rv


def get_data(hn_id: int) -> Iterator[Tuple[int, str, datetime]]:
    r = requests.get(f"https://hn.algolia.com/api/v1/items/{hn_id}")
    r.raise_for_status()
    post = r.json()
    dead = 0
    for entry in post["children"]:
        if entry["text"] is None or entry["text"] == "<p>[dead]</p>" or entry["text"] == "<p>[flagged]</p>":
            dead += 1
            continue
        yield entry["id"], entry["text"], datetime.fromtimestamp(entry["created_at_i"], tz=timezone.utc)
    print("dead>", dead)


def process_job_feed() -> Iterator[dict]:
    for item in old.process_job_feed():
        yield item


def get_entry_datetime(hn_id: int) -> datetime:
    return old.get_entry_datetime(hn_id)
