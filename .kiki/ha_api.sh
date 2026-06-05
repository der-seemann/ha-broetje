#!/usr/bin/env bash
set -euo pipefail

HA_URL="${HA_URL:-https://homeassistant.local:8123}"
HA_TOKEN_FILE="${HA_TOKEN_FILE:-/home/kiki/.openclaw/secrets/homeassistant_token.txt}"

if [[ ! -r "${HA_TOKEN_FILE}" ]]; then
  echo "HA token file not readable: ${HA_TOKEN_FILE}" >&2
  exit 1
fi

path="${1:-/api/}"
if [[ "${path}" != /* ]]; then
  path="/${path}"
fi

curl -sk \
  -H "Authorization: Bearer $(cat "${HA_TOKEN_FILE}")" \
  "${HA_URL}${path}"
