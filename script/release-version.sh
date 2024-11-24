#!/bin/bash

# Usage function to display help
usage() {
    echo "Usage: $0 <version_type> <file>"
    echo "Arguments:"
    echo " <file>         Path to an existing pyproject.toml file"
    echo ""
    echo "Remove the .devX suffix from the version in pyproject.toml file,"
    echo "and print the version to stdout."
}

main() {
    validate_arguments "$@"
    release_version "$@"
}

release_version() {
    local file="$1"

    # Extract the version line, remove .devXX suffix and write new version to the file
    awk -i inplace \
    '/version *= *".*dev[0-9]+"/ {
        # Extract major, minor, patch, and revision
        match($0, /([0-9]+\.[0-9]+\.[0-9]+)\.dev[0-9]+/, version)

        # Construct new version string
        new_version = sprintf("version = \"%s\"", version[1])

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
    "$file" # use the path passed to the script in the first argument

    # Check whether we succeeded with update and exit if e.g. pattern was not found
    if [ $? -ne 0 ]; then
        errcho "Failed updating version in $file. Is the version in correct format?"
        exit 1
    fi

    # print the updated version from pyproject.toml
    awk -F' *= *' '/^version *=/ { gsub(/"/, "", $2); print $2 }' $file
}

validate_arguments() {
    # Check if the correct number of arguments was provided
    if [[ "$#" -ne 1 ]]; then
        usage
        exit 1
    fi

    local file="$1"

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
