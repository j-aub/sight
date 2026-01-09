# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "msgspec>=0.20.0",
#     "requests>=2.32.5",
# ]
# ///

import time
from typing import List
import os

import requests
import msgspec

class File(msgspec.Struct):
    id: int
    name: str
    link: str
    type: str
    size: int

class Image(msgspec.Struct):
    id: int
    type: str
    src: str
    width: int
    height: int
    ratio: float

class Author(msgspec.Struct):
    id: int
    nickname: str
    avatar: str

class Post(msgspec.Struct):
    lang_group: int
    id: int
    language: str
    type: str
    created: int
    isAuthor: bool
    visible: bool
    isSpecial: bool
    author: Author
    likes: int
    isLiked: bool
    views: int
    doubt: bool
    featured: bool
    downloads: int
    comments: int
    isPinned: bool
    isMarketSuitable: bool
    canDelete: bool
    canEdit: bool
    description: str
    images: List[Image]
    file: File
    pbr_ready: bool
    inverted_roughness: bool

class Data(msgspec.Struct):
    list: List[Post]
    pageTitle: str
    # this is only available on page 0?
    # link: str

class Response(msgspec.Struct):
    status: str
    data: Data

def build_query(page: int):
    path = 'https://live.warthunder.com/api/feed/get_regular/'
    payload = {
        'content': 'sight',
        'sort': 'created',
        'user': '',
        # allow us to view all posts for the past 27.4 years
        'period': '10000',
        'searchString': '',
        'page': str(page),
        'featured': '0',
        'subtype': 'all',
    }
    return (path, payload)

def main() -> None:
    s = requests.Session()
    idx = 0
    post = dict()
    while True:
        print(f'doing {idx}')

#         path, payload = build_query(idx)
#         r = s.post(path, data=payload)
#         r.raise_for_status()
#         resp = r.content
#         with open(f'./output/{idx}.json', 'wb') as f:
#             f.write(resp)
        # dummy for testing
        with open(f'./output/page/{idx}.json', 'rb') as f:
            resp = f.read()

        res = msgspec.json.decode(resp, type=Response)

        # If a new post is created mid-scrape, we might see the same post
        # several times. Use a dict to eliminate duplicates.
        post |= {x.lang_group: x for x in res.data.list}

        # we've reached the end if the page is empty
        if len(res.data.list) == 0:
            print(f'end detected at {idx}')

            break

        idx += 1
        # time.sleep(0.1)

    print('writing merged file')
    # create a merged version of the data
    data = msgspec.json.encode(list(post.values()))
    with open('./output/merged.json', 'wb') as f:
        f.write(data)

    print('done')


if __name__ == "__main__":
    main()
