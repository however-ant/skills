# Usage

## Purpose

Use `scripts/restore_backup.py` to preview and restore original files from common backup filenames. The script is portable and uses only the Python standard library.

## Supported Filename Patterns

The script maps these examples to their original target names:

```text
config.json.bak                    -> config.json
config.json.bak20260501            -> config.json
config.json.bak_20260501_105702    -> config.json
config.json.backup_20260501        -> config.json
config.json_bak_20260501_105702    -> config.json
table.singletable_20260501_105702  -> table.singletable
report.txt.20260501_105702         -> report.txt
```

Timestamp forms:

```text
YYYYMMDD
YYYYMMDD_HHMMSS
YYYYMMDD-HHMMSS
YYYYMMDDHHMMSS
```

When multiple backups map to the same target, the newest backup is selected using timestamp first, then file modification time, then filename.

## Commands

Preview:

```bash
python scripts/restore_backup.py <target-directory>
```

Apply without overwriting existing target files:

```bash
python scripts/restore_backup.py <target-directory> --apply
```

Apply and overwrite existing target files:

```bash
python scripts/restore_backup.py <target-directory> --apply --overwrite
```

Apply, overwrite, and preserve current target files:

```bash
python scripts/restore_backup.py <target-directory> --apply --overwrite --keep-current
```

Scan only one directory level:

```bash
python scripts/restore_backup.py <target-directory> --no-recursive
```

## Demo

From the skill directory, copy the demo assets to a temporary writable directory and run:

```bash
python scripts/restore_backup.py assets/restore-demo
```

To test actual restore behavior without consuming the original demo assets, copy `assets/restore-demo` to a temporary folder first, then run:

```bash
python scripts/restore_backup.py <temporary-demo-copy> --apply --overwrite --keep-current
```

Expected preview operations include creating `notes.md`, `report.txt`, `settings.yaml`, `table.singletable`, and overwriting `config.json` from the newest backup.

## Migration

Copy the entire `restore_backup` skill directory to another Codex skill location. Keep `SKILL.md`, `scripts/`, `references/`, `assets/`, and `examples/` together. The bundled CLI does not rely on absolute paths or files outside the skill.
