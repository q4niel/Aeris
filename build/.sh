#!/bin/bash
projDir=$(dirname $(dirname "$(realpath "$0")"))
python -B "$projDir/build/src/main.py" 1 $projDir