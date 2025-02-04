#!/bin/bash

task="$(dirname $(realpath "$0"))"
tasks=()

if [ ! -d "$task/env" ]; then
    python3 -m venv "$task/env"
    source "$task/env/bin/activate"
    pip install -r "$task/requirements.txt"
    deactivate
fi

count=0
for file in "$task/bin"/*; do
    echo "$((count++)) | $(basename $file)"
    tasks+=("$file")
done

read -p "Run: " input

if [ "$input" -ge "0" ] && [ "$input" -lt "${#tasks[@]}" ]; then
    source "$task/env/bin/activate"
    python3 -B "${tasks[$input]}"
    deactivate
fi