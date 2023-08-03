from typing import Optional, Literal
import math


from pydantic import BaseModel
import requests

from .auth import DanbooruAuth

from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor

DANBOORU_TAGS_URL = "https://danbooru.donmai.us/tags.json"

TAG_CATEGORY = Literal[0, 1, 3, 4, 5]

TAG_CATEGORY_NAME: dict[str, TAG_CATEGORY] = {
    "general": 0,
    "artist": 1,
    # unused
    "copyright": 3,
    "character": 4,
    "meta": 5,
}

YES_OR_NO = Literal["yes", "no"]


class SearchQueryDetail(BaseModel):
    hide_empty: Optional[YES_OR_NO] = None
    order: Optional[Literal["count", "newest", "name"]] = None
    category: Optional[TAG_CATEGORY] = None
    has_artist: Optional[YES_OR_NO] = None
    has_wiki_page: Optional[YES_OR_NO] = None
    is_deprecated: Optional[YES_OR_NO] = None


class SearchQuery(BaseModel):
    page: int = 1
    commit: Optional[str] = None
    search: SearchQueryDetail


AVAILABLE_GENERAL_TAGS_SEARCH_QUERY = SearchQuery(
    search=SearchQueryDetail(
        hide_empty="yes",
        is_deprecated="no",
        order="count",
        category=TAG_CATEGORY_NAME["general"],
    )
)

AVAILABLE_CHARACTER_TAGS_SEARCH_QUERY = SearchQuery(
    search=SearchQueryDetail(
        hide_empty="yes",
        is_deprecated="no",
        order="count",
        category=TAG_CATEGORY_NAME["character"],
    )
)

AVAILABLE_COPYRIGHT_TAGS_SEARCH_QUERY = SearchQuery(
    search=SearchQueryDetail(
        hide_empty="yes",
        is_deprecated="no",
        order="count",
        category=TAG_CATEGORY_NAME["copyright"],
    )
)

AVAILABLE_ARTIST_TAGS_SEARCH_QUERY = SearchQuery(
    search=SearchQueryDetail(
        hide_empty="yes",
        is_deprecated="no",
        order="count",
        category=TAG_CATEGORY_NAME["artist"],
    )
)

AVAILABLE_META_TAGS_SEARCH_QUERY = SearchQuery(
    search=SearchQueryDetail(
        hide_empty="yes",
        is_deprecated="no",
        order="count",
        category=TAG_CATEGORY_NAME["meta"],
    )
)


class TagResponse(BaseModel):
    id: int
    name: str
    post_count: int
    category: TAG_CATEGORY
    created_at: str
    updated_at: str
    is_deprecated: bool
    words: list[str]


def compose_fetch_url(query: SearchQuery) -> str:
    url = DANBOORU_TAGS_URL
    params = query.dict(exclude_none=True)

    query = {}

    for key, value in params.items():
        if isinstance(value, dict):
            for k, v in value.items():
                query[f"{key}[{k}]"] = v
        else:
            query[key] = value

    query_str = "&".join([f"{key}={value}" for key, value in query.items()])
    url = f"{url}?{query_str}"

    return url


def fetch_api(url: str, auth: DanbooruAuth):
    headers = auth.get_headers()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def search_tags(
    query: SearchQuery, auth: DanbooruAuth, threads: int
) -> list[TagResponse]:
    # page 1 ~ 1000
    index = list(range(1, 1001))

    tags: list[TagResponse] = []

    chunks = [[] for _ in range(threads)]

    for i, num in enumerate(index):
        chunks[i % threads].append(num)

    def fetch_tags(chunk: list[int], pbar: tqdm):
        for i, page in enumerate(chunk):
            url = compose_fetch_url(query.copy(update={"page": page}))
            try:
                tags.extend(fetch_api(url, auth))
                pbar.update(1)
            except:
                # 後ろは何もしない
                pbar.update(len(chunk) - i)
                break

    with tqdm(total=len(index)) as pbar:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for chunk in chunks:
                executor.submit(fetch_tags, chunk, pbar)

            for future in futures:
                future.result()

    return tags
