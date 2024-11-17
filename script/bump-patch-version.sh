#!/bin/bash

# Usage function to display help
usage() {
    echo "The script bumps a PATCH version in the given pyproject.toml,"
    echo "adds `.dev0` suffix and prints the updated version to stdout."
    echo ""
    echo "Usage: $0 <file>"
    echo " <file>  Path to an existing pyproject.toml file"
    exit 1
}

main() {
    validate_arguments "$@"
    update_patch_version "$@"
}

update_patch_version() {
    # Extract the version line, increment revision, and replace it in the file
    awk -i inplace '
    /version *= *".*dev[0-9]+"/ {
        # Extract major, minor, patch, and revision
        match($0, /([0-9]+)\.([0-9]+)\.([0-9]+)\.dev[0-9]+/, version)
        major = version[1]
        minor = version[2]
        patch = version[3] + 1   # Increment the revision

        # Construct new version string
        new_version = sprintf("version = \"%d.%d.%d.dev0\"", major, minor, patch)

        # Replace the line with the updated version
        sub(/version *= *".*"/, new_version)

        # set found flag
        found = 1
    }
    {
        # print the processed text to stdout
        print
    }
    END {
        if (!found) exit 1
    }
    ' \
    "$1" # use the path passed to the script in the first argument

    # Check whether we succeeded with update and exit if e.g. pattern was not found
    if [ $? -ne 0 ]; then
        errcho "Failed updating version in $1. Is the version in correct format?"
        exit 1
    fi

    # print the updated version from pyproject.toml
    awk -F' *= *' '/^version *=/ { gsub(/"/, "", $2); print $2 }' $1
}

validate_arguments() {
    # Check if the correct number of arguments was provided
    if [[ "$#" -ne 1 ]]; then
        errcho "Error: Exactly one positional argument is required."
        usage
    fi

    # Assign the first positional argument to the `file` variable
    file="$1"

    # Check if the file exists
    if [[ ! -f "$file" ]]; then
        errcho "Error: File '$file' does not exist."
        exit 1
    fi
}

errcho() {
    >&2 echo $@;
}

main "$@"
