# Security boundary

This Skill is not a sandbox. Run it only in an environment where the input
videos, public pages, local scripts and installed dependencies are trusted.

## Credentials

- Do not put API keys, cookies, bearer tokens, environment files or browser
  profiles in this repository or in an evidence directory.
- Private ASR adapters must be passed explicitly from a path outside the repo.
- Never copy private adapter code or credential files into a generated report.

## Input and network boundary

- The workflow reads public pages and media downloaded from those public pages only.
- It does not access creator backends or bypass privacy, payment or permission
  controls.
- Validate downloaded media and keep generated evidence outside the source tree.

## Dependency boundary

Install only from a trusted system package manager or the official package
source documented in `references/runtime-dependencies.md`. Do not guess an
unknown package name for a missing browser or host-provided tool.
