import glob
import os
import re
from typing import List


def get_code(
    dir: str,
    out: str,
    include: List[str],
    exclude: List[str],
    exclude_files: List[str] = [],
):
    list = []
    # Open the output file for writing
    with open(out, "w") as outfile:
        # Iterate over all the ]files in the directory
        for filename in glob.glob(os.path.join(dir, "**/*"), recursive=True):
            # Make sure it's a file
            if not os.path.isfile(filename):
                continue

            # Check if the file matches any of the inclusion
            if not any(re.search(pattern, filename) for pattern in include):
                continue

            # Check if the file matches any of the exclusion patterns
            if any(re.search(pattern, filename) for pattern in exclude):
                continue

            if filename in exclude_files:
                continue

            with open(filename, "r") as f:
                list.append((len(f.read()), filename))
                # print(len(f.read()), filename)

            # Open each file and append its contents to the output file
            with open(filename, "r") as infile:
                outfile.write(f"--- FILENAME: {filename} ---\n\n")
                outfile.write(infile.read())

    list.sort(reverse=True)
    for l in list:
        print(l)

    with open(out, "r") as f:
        return f.read()


if __name__ == "__main__":
    # Set the directory path to concatenate files from
    directory = "/Users/olshansky/workspace/pocket/pocket"

    # Set the name of the file to write the concatenated code to
    output_file = "/Users/olshansky/workspace/pocket/code.txt"

    # Set the list of regular expressions to use for exclusion
    exclude_patterns = [
        # exclude files without extensions
        "^[^.]*$",
        # Don't include dependencies
        ".*vendor.*",
        "go.mod",
        "go.sum",
        # Don't include test files
        ".*_test.go",
        # Don't include changelogs
        "CHANGELOG*",
        # Don't include auto generated docs
        "client_.*.md",
        # Don't include meeting nodes
        "devlog.*.md",
        "demos",
        # Don't include supporting files
        ".*.json",
        ".*.yaml",
        ".*.sql",
        # ".*.sh",
        ".*.mk",
        # Don't include images
        ".*.gif",
        ".*.jpg",
        ".*.png",
        # Don't include generated proto files
        ".*.pb.go",
    ]

    # include_list = [".*.go", ".*.md"]
    include_list = ["utility/.*.go", "shared/.*.go", ".*.md"]

    code = get_code(directory, output_file, include_list, exclude_patterns)
    # print(code)
