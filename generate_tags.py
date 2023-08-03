import os

import json

from src.generate_tags_util import (
    search_tags,
    AVAILABLE_GENERAL_TAGS_SEARCH_QUERY,
    AVAILABLE_CHARACTER_TAGS_SEARCH_QUERY,
    AVAILABLE_COPYRIGHT_TAGS_SEARCH_QUERY,
    AVAILABLE_ARTIST_TAGS_SEARCH_QUERY,
    AVAILABLE_META_TAGS_SEARCH_QUERY,
    SearchQuery,
)
from src.auth import DanbooruAuth

import argparse


def get_tags(query: SearchQuery, auth: DanbooruAuth, threads: int, output_file: str):
    tags = search_tags(query, auth, threads)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tags, f)


def main(args):
    copyright = args.copyright
    character = args.character
    general = args.general
    artist = args.artist
    meta = args.meta

    username = args.username
    api_key = args.api_key

    output_dir = args.output_dir

    threads = args.threads

    auth = DanbooruAuth(
        username=username,
        api_key=api_key,
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if copyright:
        print("Getting copyright tags...")

        get_tags(
            AVAILABLE_COPYRIGHT_TAGS_SEARCH_QUERY,
            auth,
            threads,
            f"{output_dir}/copyright_tags.json",
        )

        print("Done")

    if character:
        print("Getting character tags...")

        get_tags(
            AVAILABLE_CHARACTER_TAGS_SEARCH_QUERY,
            auth,
            threads,
            f"{output_dir}/character_tags.json",
        )

        print("Done")

    if general:
        print("Getting general tags...")

        get_tags(
            AVAILABLE_GENERAL_TAGS_SEARCH_QUERY,
            auth,
            threads,
            f"{output_dir}/general_tags.json",
        )

        print("Done")

    if artist:
        print("Getting artist tags...")

        get_tags(
            AVAILABLE_ARTIST_TAGS_SEARCH_QUERY,
            auth,
            threads,
            f"{output_dir}/artist_tags.json",
        )

        print("Done")

    if meta:
        print("Getting meta tags...")

        get_tags(
            AVAILABLE_META_TAGS_SEARCH_QUERY,
            auth,
            threads,
            f"{output_dir}/meta_tags.json",
        )

        print("Done")

    print("All done")


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--username",
        "-u",
        type=str,
        required=True,
        help="Danbooru username",
    )

    parser.add_argument(
        "--api_key",
        type=str,
        required=True,
        help="Danbooru API key",
    )

    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        required=True,
        help="Output directory",
    )

    parser.add_argument(
        "--threads",
        "-t",
        type=int,
        default=4,
        help="Number of threads to use",
    )

    parser.add_argument(
        "--copyright",
        action="store_true",
        help="Get copyright tags",
    )

    parser.add_argument(
        "--character",
        action="store_true",
        help="Get character tags",
    )

    parser.add_argument(
        "--general",
        action="store_true",
        help="Get general tags",
    )

    parser.add_argument(
        "--artist",
        action="store_true",
        help="Get artist tags",
    )

    parser.add_argument(
        "--meta",
        action="store_true",
        help="Get meta tags",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
