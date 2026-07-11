CREATE TABLE IF NOT EXISTS learning_path_proposals (
    id TEXT PRIMARY KEY,
    goal_id TEXT REFERENCES learning_goals(id),
    proposal_json TEXT NOT NULL,
    accepted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
