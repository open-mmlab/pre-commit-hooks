# pre-commit-hooks

Some pre-commit hooks for OpenMMLab projects.

## Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/open-mmlab/pre-commit-hooks
    rev: v0.2.0  # Use the ref you want to point at
    hooks:
    -   id: check-algo-readme
    -   id: check-copyright
        args: ["dir_to_check"]  # replace the dir_to_check with your expected directory to check
    -   id: check-ecosystem-validity
```

## Hooks available

### say-hello

A template to show how to implement a pre-commit hook

### check-algo-readme

Check whether the abstract and icon exist in the algorithm readme.

- `--debug` - print details of abstract and icon in dict format.
- `--dry-run` - just dry run, igonre failed use case.
- `--model-index ${MODEL_INDEX}` - custom model-index file path.

### check-copyright

Check whether the code contains copyright

- `includes` - directory to add copyright.
- `--excludes` - exclude directory.
- `--suffixes` - copyright will be added to files with suffix.

### check-ecosystem-validity

Check the validity of the ecosystem yaml file

- `--filename` - path of the project yaml

```yaml
  - repo: https://github.com/open-mmlab/pre-commit-hooks
    rev: v0.2.1
    hooks:
    -   id: check-ecosystem-validity
        args: [projects_index.yaml]
        additional_dependencies:
          - cerberus
```
