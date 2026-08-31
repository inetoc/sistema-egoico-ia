-- ==============================================================================
-- SISTEMA EGÓICO DE IA — SCHEMA DE BANCO DE DADOS (PostgreSQL 16 + pgvector)
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(30) UNIQUE NOT NULL,
    name VARCHAR(120),
    funnel_stage VARCHAR(50) DEFAULT 'topo' CHECK (funnel_stage IN ('topo', 'meio', 'fundo', 'fechado', 'perdido')),
    persona_affinity VARCHAR(50) DEFAULT 'neutro',
    temperament VARCHAR(50) DEFAULT 'analitico',
    risk_score INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lead_profiles (
    lead_id UUID PRIMARY KEY REFERENCES leads(id) ON DELETE CASCADE,
    core_pain_points TEXT[],
    buying_desires TEXT[],
    fears_objections TEXT[],
    budget_range VARCHAR(50),
    decision_maker BOOLEAN DEFAULT TRUE,
    ego_notes TEXT,
    last_profiled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    sender VARCHAR(20) NOT NULL CHECK (sender IN ('user', 'agent_ego')),
    content TEXT NOT NULL,
    msg_type VARCHAR(20) DEFAULT 'text' CHECK (msg_type IN ('text', 'audio', 'image', 'document')),
    message_id_evolution VARCHAR(100),
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cognitive_debates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    incoming_message TEXT NOT NULL,
    id_thesis TEXT NOT NULL,
    superego_audit TEXT NOT NULL,
    ego_synthesis TEXT NOT NULL,
    guardrails_passed BOOLEAN DEFAULT TRUE,
    latency_ms INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_leads_phone ON leads(phone);
CREATE INDEX IF NOT EXISTS idx_messages_lead_id ON messages(lead_id, sent_at DESC);
CREATE INDEX IF NOT EXISTS idx_knowledge_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE OR REPLACE FUNCTION match_knowledge (
    query_embedding vector(1536),
    match_threshold FLOAT,
    match_count INT
)
RETURNS TABLE (
    id UUID,
    title VARCHAR(200),
    content TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        kb.id,
        kb.title,
        kb.content,
        1 - (kb.embedding <=> query_embedding) AS similarity
    FROM knowledge_base kb
    WHERE 1 - (kb.embedding <=> query_embedding) > match_threshold
    ORDER BY kb.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
