export async function ensureSharedCalculationsTable(db: D1Database) {
  await db.batch([
    db.prepare(`CREATE TABLE IF NOT EXISTS shared_calculations (
      id TEXT PRIMARY KEY NOT NULL,
      created_at TEXT NOT NULL,
      schema_version TEXT NOT NULL,
      project_name TEXT NOT NULL,
      consent_version TEXT NOT NULL,
      config_json TEXT NOT NULL,
      result_json TEXT NOT NULL
    )`),
    db.prepare(`CREATE INDEX IF NOT EXISTS idx_shared_calculations_created_at
      ON shared_calculations(created_at)`),
  ]);
}
