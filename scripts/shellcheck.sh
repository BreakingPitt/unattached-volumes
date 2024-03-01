#!/usr/bin/env bash

set -o errexit
set -o pipefail

[[ "${DEBUG}" == 'true' ]] && set -o xtrace

function shellcheck_command() {
    # koalaman/shellcheck:v0.9.0
    local docker_image='koalaman/shellcheck@sha256:a527e2077f11f28c1c1ad1dc784b5bc966baeb3e34ef304a0ffa72699b01ad9c'

    docker run                      \
           --tty                    \
           --rm                     \
           -v "${PWD}":"${PWD}"     \
           -w "${PWD}"              \
           -u "$(id -u)":"$(id -g)" \
           -e HOME="${PWD}"         \
           ${docker_image}          \
           --color=always           \
           --format=tty             \
           -x                       \
           "$@"
}

function main() {
    local current_dir
    current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

    pushd "${current_dir}"/..
        SCRIPT_FILES=$(find . -name "*.sh" -not -path "*/target/*")
        readonly SCRIPT_FILES

        # shellcheck disable=SC2086
        shellcheck_command ${SCRIPT_FILES}
    popd
}

main