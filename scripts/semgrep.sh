#!/usr/bin/env bash

set -o errexit
set -o pipefail

[[ "${DEBUG}" == 'true' ]] && set -o xtrace

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function semgrep_command() {
    # returntocorp/semgrep:2-0.8
    local docker_image="returntocorp/semgrep@sha256:8b7a3b283aed5facab9c644c031d9ee7b7d5013279dfb4fcac91f7c662768003"

    docker run                        \
      -u "$(id -u)":"$(id -g)"        \
      -v "${HOME}"/.semgrep:/.semgrep \
      -v "${PWD}":"${PWD}"            \
      -w "${PWD}"                     \
      --rm                            \
      --tty                           \
      -e HOME="${PWD}"                \
      "${docker_image}"               \
      "$@"
}

pushd "${CURRENT_DIR}"/..
    semgrep_command                                \
      semgrep                                      \
      scan                                         \
      --config=p/r2c-security-audit                \
      --error                                      \
      --force-color                                \
      --metrics off                                \
      --json                                       \
      --severity WARNING                           \
      --severity ERROR                             \
      --time                                       \
      --use-git-ignore                             \
      --verbose                                    \
      mp3_duplicate_finder                         \
    > ./scan_results.json

popd