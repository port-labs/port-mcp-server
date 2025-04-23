#!/bin/bash

# Check if the version is set
if [ -z "$VERSION" ]; then
    echo "VERSION is not set. Please set the VERSION environment variable."
    exit 1
fi
if [ -z "$TWINE_API" ]; then
    echo "TWINE_API_KEY is not set. Please set the TWINE_API_KEY environment variable."
    exit 1
fi

make release;

