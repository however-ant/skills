---
name: restore-backup
description: Independently preview and restore original files from backup filenames. Use when the user asks to recover, restore, roll back, or revert files from backups; restore .bak/.backup files; remove backup or timestamp suffixes; recover files named like config.json.bak_20260501_105702, table.singletable_20260501_105702, or report.txt.20260501_105702. Always run a preview first and ask for user confirmation before applying file changes.
---

# Restore Backup

Use this skill to restore original files from backup filenames with the bundled CLI script. The skill is self-contained; do not depend on project-local `restore_backup.py` files outside this skill.

## Workflow

1. Resolve the target directory from the user's request. Use the current working directory when no target is specified.
2. Run a preview with the bundled script:

```bash
python .agents/skills/restore_backup/scripts/restore_backup.py <target-directory>
```

3. Summarize the preview. Call out every `[overwrite]` entry because it affects an existing target file.
4. Ask for explicit confirmation before any command containing `--apply`.
5. Prefer preserving existing targets when overwriting:

```bash
python .agents/skills/restore_backup/scripts/restore_backup.py <target-directory> --apply --overwrite --keep-current
```

6. After execution, report restored files, skipped existing targets, preserved current files, and failures.

## Command Choices

Use dry-run preview by default:

```bash
python .agents/skills/restore_backup/scripts/restore_backup.py <target-directory>
```

Restore only files whose target does not already exist:

```bash
python .agents/skills/restore_backup/scripts/restore_backup.py <target-directory> --apply
```

Overwrite existing target files after confirmation:

```bash
python .agents/skills/restore_backup/scripts/restore_backup.py <target-directory> --apply --overwrite
```

Overwrite while preserving current target files:

```bash
python .agents/skills/restore_backup/scripts/restore_backup.py <target-directory> --apply --overwrite --keep-current
```

Scan only one directory level:

```bash
python .agents/skills/restore_backup/scripts/restore_backup.py <target-directory> --no-recursive
```

## References

- Read `references/usage.md` when the user asks what patterns are supported, how to run a demo, or how to migrate the skill.
- Read `references/troubleshooting.md` when Python, path, permission, overwrite, encoding, or validation problems occur.

## Safety Rules

- Never apply changes before showing a preview.
- Never use `--overwrite` unless the user explicitly confirms overwriting.
- Use `--keep-current` when the user wants recovery but has not asked to delete existing target files.
- Do not hand-write rename/delete commands while the bundled script can perform the operation.
- Do not modify the bundled script during a restoration task unless the user asks to change tool behavior.
