# NEC Inspection App - Project Memory

## Database Architecture
- **PostgreSQL only** - migrated from SQLite to `company_ops` database at `192.168.40.11:5432`
- Schemas: `nec`, `materials`, `shared` (search_path includes all + public)
- Auth chain: env vars (`NEC_PG_*`) > Windows Credential Manager (`keyring`) > session config > ValueError
- Connection pool in `src/database/connection.py` (singleton via `_get_shared_pool()`)
- Schema init runs once per shared pool (guarded by `_schema_initialized` flag in operations.py)
- `psycopg2.sql.Identifier` used for table name interpolation (prevents SQL injection)
- SAVEPOINTs used in `_execute_sql_file` and `_apply_migrations` for isolated error handling

## Key PostgreSQL Patterns
- `%s` placeholders (not `?`), `ILIKE` (not `LIKE`), `RETURNING id` (not `lastrowid`)
- `RealDictCursor` - rows are dicts, use `row['column']` not `row[0]`
- `NOW() - INTERVAL '30 days'` (not `datetime('now', '-30 days')`)
- `information_schema.tables/columns` (not `sqlite_master`/`PRAGMA`)
- Subqueries require aliases (`AS sub`) in PostgreSQL
- COUNT/SUM queries need `AS` aliases for RealDictCursor (`COUNT(*) AS cnt`)

## Code Style (CLAUDE.md)
- **ASCII only** - no emojis/unicode. Use `SUCCESS:`, `ERROR:`, `->`
- PEP 8, type hints, docstrings on functions/classes

## Test Structure
- Tests in `tests/unit/database/` - 78 tests, all passing
- Mock pattern: `_make_mock_pool()` + `_make_db_manager(pool)` for isolated DB tests
- `psycopg2-binary` must be installed in venv
- Source scanning tests verify no SQLite patterns remain in migrated files

## Migration Status (Phases 1-7 complete)
- All SQLite patterns converted across ~30 files
- Migration scripts: `scripts/migrate_sqlite_to_pg.py`, `scripts/verify_migration.py`
- Original SQLite data preserved at `data/database/inspections.db` (19.6 MB)
