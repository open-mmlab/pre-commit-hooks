# MMPrecommit

Some pre-commit hooks for OpenMMLab projects.

## Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v0.0.0  # Use the ref you want to point at
    hooks:
    -   id: say-hello
```
## Hooks available

### demo

A template to show how to implement a pre-commit hook

