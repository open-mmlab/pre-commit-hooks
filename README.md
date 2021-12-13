# MMPrecommit

Some pre-commit hooks for OpenMMLab projects.

## Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/zhouzaida/mmprecommit
    rev: v0.1.0  # Use the ref you want to point at
    hooks:
    -   id: say-hello
```
## Hooks available

### say-hello

A template to show how to implement a pre-commit hook

### check-algo-readme

Check whether the abstract and icon exist in the algorithm readme.

* `--debug` - print details of abstract and icon in dict format.
* `--dry-run` - just dry run, igonre failed use case.
* `--model-index ${MODEL_INDEX}` - custom model-index file path.
