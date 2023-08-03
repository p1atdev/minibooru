import json


from src.generate_tags_util import TagResponse

import argparse


def main(args):
    path_to_file = args.path_to_file

    with open(path_to_file, "r", encoding="utf-8") as f:
        tags = [TagResponse(**tag) for tag in json.load(f)]

    # sort by count
    tags.sort(key=lambda tag: tag.post_count, reverse=True)

    # show top 10 and bottom 10
    print("Top 10 by post count:")
    for tag in tags[:10]:
        print(f"- {tag.name}: {tag.post_count}")

    print("Bottom 10 by post count:")
    for tag in tags[-10:]:
        print(f"- {tag.name}: {tag.post_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "path_to_file",
        type=str,
        help="Path to the JSON file containing the tags.",
    )

    args = parser.parse_args()

    main(args)
