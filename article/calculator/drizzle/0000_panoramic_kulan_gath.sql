CREATE TABLE `shared_calculations` (
	`id` text PRIMARY KEY NOT NULL,
	`created_at` text NOT NULL,
	`schema_version` text NOT NULL,
	`project_name` text NOT NULL,
	`consent_version` text NOT NULL,
	`config_json` text NOT NULL,
	`result_json` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `idx_shared_calculations_created_at` ON `shared_calculations` (`created_at`);