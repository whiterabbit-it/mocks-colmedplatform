-- feedback_comments table for VitaCore Mocks feedback toolbox
CREATE TABLE IF NOT EXISTS public.feedback_comments (
  id           UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_name    TEXT NOT NULL,
  user_email   TEXT NOT NULL,
  page_path    TEXT NOT NULL,
  page_title   TEXT,
  element_hint TEXT,
  comment      TEXT NOT NULL,
  created_at   TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS
ALTER TABLE public.feedback_comments ENABLE ROW LEVEL SECURITY;

-- Policy: anyone (anon) can insert
CREATE POLICY "anon_insert" ON public.feedback_comments
  FOR INSERT TO anon WITH CHECK (true);

-- Policy: anyone can read (needed for feedback panel and badge count)
CREATE POLICY "anon_select" ON public.feedback_comments
  FOR SELECT TO anon USING (true);
