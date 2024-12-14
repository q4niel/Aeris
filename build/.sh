#!/bin/bash
projDir=$(dirname $(dirname "$(realpath "$0")"))
python3 -B "$projDir/build/src/main.py" $projDir