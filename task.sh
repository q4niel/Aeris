#!/bin/bash

tasks=()

for py in "$(dirname $(realpath "$0"))/tsk"/*.py; do
    if grep -q "if __name__ == \"__main__\": main()" "$py"; then
        tasks+=("$py")
    fi
done

count=0
for task in "${tasks[@]}"; do
    echo "$((count++)) | $(basename $task)"
done

read -p "Run: " input

if [ "$input" -ge "0" ] && [ "$input" -lt "${#tasks[@]}" ]; then
    python3 -B "${tasks[$input]}"
fi