import json


from src.generate_tags_util import TagResponse

import argparse


def main(args):
    path_to_file = args.path_to_file
    output_file = args.output_file

    with open(path_to_file, "r", encoding="utf-8") as f:
        tags = [TagResponse(**tag) for tag in json.load(f)]

    # sort by count
    tags.sort(key=lambda tag: tag.post_count, reverse=True)

    tag_names = [tag.name for tag in tags]

    # write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tag_names))

    print(f"Exported {len(tag_names)} tags to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "path_to_file",
        type=str,
        help="Path to the JSON file containing the tags.",
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Path to the output file.",
    )

    args = parser.parse_args()

    main(args)
