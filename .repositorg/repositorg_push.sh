#!/usr/bin/env bash
# This script should be kept and run on the data acquisition machine.
# Given the nomenclature below: example-source and NOT analysishost!
rsync -avP /incoming/data anaylsishost:/var/tmp/repositorg/example-source
ssh analysishost ~/.repositorg/sources/example-source_post-hook.sh
