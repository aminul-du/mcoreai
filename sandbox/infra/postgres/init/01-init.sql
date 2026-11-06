-- =============================================================================
-- PostgreSQL init — evidence schema, pgvector extension, audit table
-- Runs on first container start only (docker-entrypoint-initdb.d)
-- =============================================================================

-- Enable pgvector (optional adapter; harmless if unused)
CREATE EXTENSION IF NOT EXISTS vector;

-- Evidence store
CREATE TABLE IF NOT EXISTS evidence (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source      TEXT NOT NULL,          -- microsoft | google | github | local
    doc_id      TEXT NOT NULL,
    content     TEXT,
    embedding   VECTOR(1536),
    controls    JSONB DEFAULT '[]'::jsonb,  -- CIA, SOC2, ISO27001, NIST tags
    created_at  TIMESTAMPTZ DEFAULT now(),
    updated_at  TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_evidence_source ON evidence(source);
CREATE INDEX IF NOT EXISTS idx_evidence_controls ON evidence USING gin(controls);

-- Audit log (Access events, policy decisions)
CREATE TABLE IF NOT EXISTS audit_log (
    id          BIGSERIAL PRIMARY KEY,
    event_type  TEXT NOT NULL,          -- auth | policy | ingest | access
    actor       TEXT,
    action      TEXT,
    resource    TEXT,
    decision    TEXT,
    metadata    JSONB DEFAULT '{}'::jsonb,
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_type ON audit_log(event_type);
