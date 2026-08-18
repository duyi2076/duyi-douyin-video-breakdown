#!/usr/bin/env bash
set -euo pipefail

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
skill_name="duyi-douyin-video-breakdown-v3"
skills_root="${DUYI_SKILLS_ROOT:-${HOME:?}/.agents/skills}"
target="${skills_root}/${skill_name}"

case "$target" in
  /|"$HOME"|"$HOME"/)
    echo "Refusing an overly broad install target: $target" >&2
    exit 1
    ;;
esac

if [ ! -f "$repo_root/SKILL.md" ]; then
  echo "SKILL.md is missing from the package" >&2
  exit 1
fi

if [ -e "$target" ] || [ -L "$target" ]; then
  echo "Refusing to overwrite existing path: $target" >&2
  exit 1
fi

mkdir -p "$skills_root"
staging="$(mktemp -d "${skills_root}/.${skill_name}.install.XXXXXX")"
trap 'rm -rf "$staging"' EXIT
cp -R "$repo_root/." "$staging/"
mv "$staging" "$target"

for entry in .claude .codex .hermes; do
  mkdir -p "$HOME/$entry/skills"
  link="$HOME/$entry/skills/$skill_name"
  if [ -e "$link" ] || [ -L "$link" ]; then
    echo "Refusing to overwrite existing link: $link" >&2
    exit 1
  fi
  ln -s "../../.agents/skills/$skill_name" "$link"
done

echo "Installed $skill_name to $target"
