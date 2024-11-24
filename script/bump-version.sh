#!/bin/bash

# Usage function to display help
usage() {
    echo "Usage: $0 <version_type> <file>"
    echo "Arguments:"
    echo " <version_type> One of: major, minor, patch, revision"
    echo " <file>         Path to an existing pyproject.toml file"
    echo ""
    echo "Increments a version in the given pyproject.toml."
    echo "Revision bump increments the development revision."
    echo "Major, minor or patch bump increments the requested version,"
    echo "and zeroes the following sub-versions."
    echo ""
    echo "The script updates pyproject.toml and prints the"
    echo "updated version to stdout."
}

main() {
    validate_arguments "$@"
    update_version "$@"
}

update_version() {
    local version_type="$1"
    local file="$2"

    # Extract the version line, increment major/minor/patch/revision, and replace it in the file
    awk -i inplace -v version_type="$version_type" \
    '/^version *= *"[0-9]+\.[0-9]+\.[0-9]+\.dev[0-9]+"$/ {
        # Extract major, minor, patch, and revision
        match($0, /([0-9]+)\.([0-9]+)\.([0-9]+)\.dev([0-9]+)/, version)
        major = version[1]
        minor = version[2]
        patch = version[3]
        revision = version[4]

        if (version_type == "major") {
            major++
            minor = 0
            patch = 0
            revision = 0
        } else if (version_type == "minor") {
            minor++
            patch = 0
            revision = 0
        } else if (version_type == "patch") {
            patch++
            revision = 0
        } else if (version_type == "revision") {
            revision++
        }

        # Construct new version string
        new_version = sprintf("version = \"%d.%d.%d.dev%d\"", major, minor, patch, revision)

        # Replace the line with the updated version
        sub(/version *= *".*"/, new_version)

        # set found flag
        found = 1
    }
    /^version *= *"[0-9]+\.[0-9]+\.[0-9]+"$/ {
        # Extract major, minor, patch, and revision
        match($0, /([0-9]+)\.([0-9]+)\.([0-9]+)/, version)
        major = version[1]
        minor = version[2]
        patch = version[3]

        if (version_type == "major") {
            major++
            minor = 0
            patch = 0
        } else if (version_type == "minor") {
            minor++
            patch = 0
        } else if (version_type == "patch") {
            patch++
        } else if (version_type == "revision") {
            printf "Cant bump missing revision on version %d.%d.%d\n", major, minor, patch > "/dev/stderr"
            exit 1
        }

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
    if [[ "$#" -ne 2 ]]; then
        usage
        exit 1
    fi

    local version_type="$1"
    local file="$2"

    # Check if the file exists
    if [[ ! -f "$file" ]]; then
        errcho "Error: File '$file' does not exist."
        exit 1
    fi

    # Check if the version type is valid
    if [[ \
          "$version_type" != "major" \
          && "$version_type" != "minor" \
          && "$version_type" != "patch" \
          && "$version_type" != "revision"
       ]]; then
        errcho 'Error: Invalid version_type "$version_type" Must be one of: major, minor, patch revision.'
        usage
        exit 1
    fi
}

errcho() {
    >&2 echo $@;
}

main "$@"
