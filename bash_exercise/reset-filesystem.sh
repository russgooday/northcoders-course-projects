#!/usr/bin/env bash

RED='\e[31m'
GREEN='\e[32m'
DEFAULT='\e[0m'

CURR_DIR=$(basename "$(pwd)")

if [ "$CURR_DIR" != "bash_exercise" ]; then
  echo -e "$RED ❗ To run this script you need to be in the bash_exercise directory$DEFAULT"
else
  echo -e "$RED > Removing current nc-filesystem 🗑️$DEFAULT"
  rm -rf filesystem

  echo -e "$GREEN > Restoring filesystem backup ✅$DEFAULT"
  mkdir filesystem && cp -r ./filesystem-backup/* ./filesystem/
fi
