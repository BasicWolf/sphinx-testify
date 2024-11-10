#!/bin/bash


# Usage function to display help
usage() {
    echo "The script bumps a DEVELOPMENT version revision in the given pyproject.toml"
    echo ""
    echo "Usage: $0 <file>"
    echo " <file>  Path to an existing pyproject.toml file"
    exit 1
}

main() {
    validate_arguments "$@"
    update_dev_version "$@"
}

update_dev_version() {
    # Extract the version line, increment revision, and replace it in the file
    awk -i inplace '
    /version *= *".*dev[0-9]+"/ {
        # Extract major, minor, patch, and revision
        match($0, /([0-9]+)\.([0-9]+)\.([0-9]+)dev([0-9]+)/, version)
        major = version[1]
        minor = version[2]
        patch = version[3]
        revision = version[4] + 1  # Increment the revision

        # Construct new version string
        new_version = sprintf("version = \"%d.%d.%ddev%d\"", major, minor, patch, revision)

        # Replace the line with the updated version
        sub(/version *= *".*"/, new_version)
    }
    # print to stdout
    { print }' \
    "$1" # use the path passed to the script in the first argument
}

validate_arguments() {
    # Check if the correct number of arguments was provided
    if [[ "$#" -ne 1 ]]; then
        echo "Error: Exactly one positional argument is required."
        usage
    fi

    # Assign the first positional argument to the `file` variable
    file="$1"

    # Check if the file exists
    if [[ ! -f "$file" ]]; then
        echo "Error: File '$file' does not exist."
        exit 1
    fi
}

main "$@"
