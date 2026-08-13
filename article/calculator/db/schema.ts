import { index, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const sharedCalculations = sqliteTable(
  "shared_calculations",
  {
    id: text("id").primaryKey(),
    createdAt: text("created_at").notNull(),
    schemaVersion: text("schema_version").notNull(),
    projectName: text("project_name").notNull(),
    consentVersion: text("consent_version").notNull(),
    configJson: text("config_json").notNull(),
    resultJson: text("result_json").notNull(),
  },
  (table) => [index("idx_shared_calculations_created_at").on(table.createdAt)],
);
