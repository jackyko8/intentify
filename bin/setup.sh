#!/bin/bash

# Use `source bin/setup.sh` from the repo root to set these environment variables

export STACK_NAME=intentify
export S3_PATH=intentify-deployment-309062441977/src/streamlit

# For pip installs
export TMPDIR=$(pwd)/_tmp
test ! -d $TMPDIR && mkdir -p $TMPDIR
