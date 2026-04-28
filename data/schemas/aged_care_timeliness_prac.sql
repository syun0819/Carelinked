CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS aged_care_timeliness_prac (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Covariate group, e.g. 'Sex', 'Priority level', 'Dementia status'.
    -- Forward-filled from category-header rows in the source xlsx.
    category TEXT NOT NULL,

    -- The specific value within the category, e.g. 'Women', 'High',
    -- 'Dementia'. Unique within a category.
    value TEXT NOT NULL,

    -- Event rate ratio from the competing-risks regression (Fine-Gray)
    -- for the 'PRAC only' approval group. >1 means shorter elapsed time
    -- to receive permanent residential aged care vs. the reference group;
    -- <1 means longer. Reference rows are exactly 1.
    event_rate_ratio NUMERIC(6,3) NOT NULL,

    -- 95% confidence interval bounds. NULL on reference rows because the
    -- source publishes blanks for the reference category in each group.
    lower_ci NUMERIC(6,3),
    upper_ci NUMERIC(6,3),

    -- TRUE when this is the reference category (event_rate_ratio = 1).
    -- The calculator should skip multiplying by reference rows.
    is_reference BOOLEAN NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (category, value)
);

CREATE INDEX IF NOT EXISTS idx_aged_care_timeliness_prac_category
    ON aged_care_timeliness_prac(category);
