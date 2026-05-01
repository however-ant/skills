# Troubleshooting

## Python Command Not Found

Use an available Python interpreter:

```bash
python scripts/restore_backup.py <target-directory>
py scripts/restore_backup.py <target-directory>
python3 scripts/restore_backup.py <target-directory>
```

If Codex is sandboxed and cannot access a user-local Python installation, ask for permission to run the configured interpreter outside the sandbox.

## No Backup Files Matched

Check whether filenames match supported patterns in `references/usage.md`. Files created by this tool with `.before_restore_` are intentionally ignored.

## Existing Target Files Were Skipped

This is expected without `--overwrite`. Run a preview again, confirm the overwrite list with the user, then apply with:

```bash
python scripts/restore_backup.py <target-directory> --apply --overwrite --keep-current
```

## Keep Current Requires Overwrite

`--keep-current` only makes sense when replacing existing targets. Use it with `--overwrite`:

```bash
python scripts/restore_backup.py <target-directory> --apply --overwrite --keep-current
```

## Wrong Backup Selected

The script picks the newest backup by embedded timestamp, then modification time, then filename. If a project uses a different backup naming scheme, preview first and do not apply until the mapping is confirmed.

## Permission Errors

Check whether target files are read-only, locked by another process, or outside the writable workspace. Do not bypass permissions with manual delete commands; resolve the path or permission issue first.

## Encoding Issues In Output

The script prints ASCII status labels and filesystem paths. If a terminal displays non-ASCII filenames incorrectly, the restore logic can still be correct; verify with directory listing commands that support UTF-8.
