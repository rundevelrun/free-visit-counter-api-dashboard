-- Add new columns to visit_logs table
ALTER TABLE visit_logs ADD COLUMN IF NOT EXISTS page_path VARCHAR(255);
ALTER TABLE visit_logs ADD COLUMN IF NOT EXISTS page_title VARCHAR(255);
ALTER TABLE visit_logs ADD COLUMN IF NOT EXISTS referrer VARCHAR(255);
ALTER TABLE visit_logs ADD COLUMN IF NOT EXISTS search_query VARCHAR(255);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_visit_logs_page_path ON visit_logs (page_path);
CREATE INDEX IF NOT EXISTS idx_visit_logs_referrer ON visit_logs (referrer);
