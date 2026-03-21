# Versioning Policy

This project uses **Semantic Versioning**:

- **MAJOR**: Breaking changes
- **MINOR**: New features, no breaking changes
- **PATCH**: Fixes and small improvements

## Example

`v0.1.0`

- `0` → pre-release / early development
- `1` → first feature milestone
- `0` → no patches yet

## Tagging

Tags are created from the `main` branch:

    git tag -a vX.Y.Z -m "Release vX.Y.Z"
    git push origin vX.Y.Z
