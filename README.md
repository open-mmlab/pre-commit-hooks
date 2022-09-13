# pre-commit-hooks

Some pre-commit hooks for OpenMMLab projects.

## Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/open-mmlab/pre-commit-hooks
    rev: v0.4.0  # Use the ref you want to point at
    hooks:
    -   id: check-algo-readme
    -   id: check-copyright
        args: ["dir_to_check"]  # replace the dir_to_check with your expected directory to check
    -   id: check-ecosystem-validity
        args: [projects_index.yaml]
        additional_dependencies:
          - cerberus
    -   id: remove-improper-eol-in-cn-docs
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

- `filename` - path of the project yaml

```yaml
  - repo: https://github.com/open-mmlab/pre-commit-hooks
    rev: v0.4.0
    hooks:
    -   id: check-ecosystem-validity
        args: [projects_index.yaml]
        additional_dependencies:
          - cerberus
```

### remove-improper-eol-in-cn-docs

Remove end-of-line characters that split natural paragraphs in Chinese docs.

This helps resolve extra whitespaces in Chinese Markdown docs described [here](https://stackoverflow.com/questions/8550112/prevent-workaround-browser-converting-n-between-lines-into-space-for-chinese/8551033#8551033), as a long-standing HTML rendering issue. For example,

> 这是一个，
> 像诗一样的
> 测试

will be changed to:

> 这是一个，像诗一样的测试

Usage:

```yaml
  - repo: https://github.com/open-mmlab/pre-commit-hooks
    rev: v0.4.0
    hooks:
    -   id: remove-improper-eol-in-cn-docs
```
