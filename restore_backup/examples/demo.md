# Demo

This skill includes demo input files in `assets/restore-demo`.

Run a preview from the skill directory:

```bash
python scripts/restore_backup.py assets/restore-demo
```

To test real restoration without changing the source demo files, copy `assets/restore-demo` to a temporary directory and run:

```bash
python scripts/restore_backup.py <temporary-demo-copy> --apply --overwrite --keep-current
```

Expected behavior:

```text
config.json.bak_20260501_105702 -> config.json
notes.md_bak_20260501_105702 -> notes.md
report.txt.20260501_105702 -> report.txt
settings.yaml.backup_20260501 -> settings.yaml
table.singletable_20260501_105702 -> table.singletable
```
