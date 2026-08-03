#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
src_dir="${1:-${script_dir}/custom_components/broetje_heating}"
dst_dir="${2:-/home/kiki/HA/custom_components/broetje_heating}"

if [[ ! -d "$src_dir" ]]; then
  echo "Source directory missing: $src_dir" >&2
  exit 1
fi

mkdir -p "$dst_dir"
rsync -a --delete "${src_dir}/" "${dst_dir}/"

if diff -r "$src_dir" "$dst_dir" >/dev/null; then
  echo "0 differences"
else
  echo "Deploy diff mismatch between $src_dir and $dst_dir" >&2
  diff -r "$src_dir" "$dst_dir" >&2 || true
  exit 1
fi
