-- ============================================================
-- Aegis — PostgreSQL Database Initialization
-- Runs automatically via Docker Compose entrypoint
-- ============================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================================
-- Core Tables: Employee & Organizational Data
-- ============================================================

CREATE TABLE IF NOT EXISTS employees (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR     UNIQUE NOT NULL,
    full_name       VARCHAR     NOT NULL,
    department      VARCHAR     NOT NULL,
    role_title      VARCHAR     NOT NULL,
    seniority_tier  INTEGER     NOT NULL CHECK (seniority_tier BETWEEN 1 AND 5),
    location_city   VARCHAR     NOT NULL,
    location_country VARCHAR    NOT NULL,
    manager_id      UUID        REFERENCES employees(id),
    hire_date       DATE        NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now(),
    deleted_at      TIMESTAMPTZ  -- soft delete
);

CREATE TABLE IF NOT EXISTS vendors (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    canonical_name  VARCHAR     UNIQUE NOT NULL,
    aliases         TEXT[]      NOT NULL DEFAULT '{}',
    category        VARCHAR,
    verified        BOOLEAN     DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================================
-- Expense Records
-- ============================================================

CREATE TABLE IF NOT EXISTS expenses (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    idempotency_key     VARCHAR     UNIQUE NOT NULL,
    employee_id         UUID        NOT NULL REFERENCES employees(id),
    vendor_id           UUID        REFERENCES vendors(id),

    -- Extracted data
    merchant_name_raw   VARCHAR     NOT NULL,
    transaction_date    DATE        NOT NULL,
    currency            CHAR(3)     NOT NULL,
    subtotal            NUMERIC(12,2) NOT NULL,
    tax_amount          NUMERIC(12,2),
    tip_amount          NUMERIC(12,2),
    total_amount        NUMERIC(12,2) NOT NULL,
    category            VARCHAR     NOT NULL,
    line_items          JSONB       DEFAULT '[]',
    justification       TEXT,

    -- Processing metadata
    receipt_file_url    VARCHAR     NOT NULL,
    extraction_model    VARCHAR,
    extraction_confidence NUMERIC(3,2),
    extraction_warnings TEXT[],

    -- Decision
    status              VARCHAR     NOT NULL DEFAULT 'SUBMITTED'
                        CHECK (status IN ('SUBMITTED','PROCESSING','APPROVED',
                               'REJECTED','NEEDS_REMEDIATION','ESCALATED','WITHDRAWN')),
    final_decision      VARCHAR     CHECK (final_decision IN ('APPROVED','REJECTED','ESCALATED')),
    decided_at          TIMESTAMPTZ,

    -- Audit
    created_at          TIMESTAMPTZ DEFAULT now(),
    updated_at          TIMESTAMPTZ DEFAULT now(),
    deleted_at          TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_expenses_employee ON expenses(employee_id);
CREATE INDEX IF NOT EXISTS idx_expenses_status ON expenses(status);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(transaction_date);
CREATE INDEX IF NOT EXISTS idx_expenses_idempotency ON expenses(idempotency_key);

-- ============================================================
-- Audit Trail (Immutable Event Log)
-- ============================================================

CREATE TABLE IF NOT EXISTS audit_events (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    expense_id      UUID        NOT NULL REFERENCES expenses(id),
    event_type      VARCHAR     NOT NULL,
    agent_name      VARCHAR,
    payload         JSONB       NOT NULL,
    llm_model_used  VARCHAR,
    llm_tokens_in   INTEGER,
    llm_tokens_out  INTEGER,
    latency_ms      INTEGER,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_audit_expense ON audit_events(expense_id);
CREATE INDEX IF NOT EXISTS idx_audit_type ON audit_events(event_type);

-- ============================================================
-- Remediation / Negotiation Logs
-- ============================================================

CREATE TABLE IF NOT EXISTS remediation_sessions (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    expense_id      UUID        NOT NULL REFERENCES expenses(id),
    round_number    INTEGER     NOT NULL DEFAULT 1,
    discrepancy     JSONB       NOT NULL,
    agent_message   TEXT        NOT NULL,
    employee_response TEXT,
    crm_validation  JSONB,
    outcome         VARCHAR     CHECK (outcome IN ('RESOLVED','RE_EVALUATE','ESCALATE','TIMEOUT')),
    created_at      TIMESTAMPTZ DEFAULT now(),
    responded_at    TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_remediation_expense ON remediation_sessions(expense_id);

-- ============================================================
-- Fraud Flags
-- ============================================================

CREATE TABLE IF NOT EXISTS fraud_flags (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    expense_id      UUID        NOT NULL REFERENCES expenses(id),
    flag_type       VARCHAR     NOT NULL CHECK (flag_type IN ('DUPLICATE', 'ANOMALY', 'AI_GENERATED')),
    confidence      FLOAT       NOT NULL,
    duplicate_of    UUID        REFERENCES expenses(id),
    similarity_score FLOAT,
    isolation_score  FLOAT,
    flagged_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fraud_expense ON fraud_flags(expense_id);

-- ============================================================
-- Seed: Insert initial vendor data
-- ============================================================

INSERT INTO vendors (canonical_name, aliases, category, verified) VALUES
    ('Uber', ARRAY['Uber BV', 'Uber Trip', 'UBER*', 'Uber Technologies'], 'transport', TRUE),
    ('Deliveroo', ARRAY['DELIVEROO', 'Deliveroo UK'], 'meals', TRUE),
    ('Premier Inn', ARRAY['Premier Inn Hotels', 'PREMIER INN', 'Whitbread PLC'], 'accommodation', TRUE),
    ('Pret A Manger', ARRAY['PRET', 'Pret a Manger UK', 'PRET A MANGER'], 'meals', TRUE),
    ('Tesco', ARRAY['TESCO STORES', 'Tesco PLC', 'TESCO EXPRESS'], 'office_supplies', TRUE)
ON CONFLICT (canonical_name) DO NOTHING;
