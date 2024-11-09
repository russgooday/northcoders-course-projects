#!/usr/bin/env bash
# colours
NORMAL=$(tput sgr0 setaf 15)
PRIMARY=$(tput setaf 10 bold)
SECONDARY=$(tput setaf 9 bold)

# To set the local bin path, the script needs to be executed with source
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "${SECONDARY}Script needs to be executed with source e.g.$ ${PRIMARY}source ${BASH_SOURCE[0]}"
    exit 1
fi

# Set PATH so it includes local bin folder
if [ -d "./bin" ] ; then
    PATH="$(pwd)/bin:$PATH"
fi

sudo apt-get update
# Install jq command-line JSON processor - https://jqlang.github.io/jq/
sudo apt-get install jq
