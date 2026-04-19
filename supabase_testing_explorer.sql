-- =============================================
-- 4) testing_explorer
-- =============================================
CREATE TABLE IF NOT EXISTS public.testing_explorer (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  test_name TEXT NOT NULL,
  test_input JSONB,
  test_output JSONB,
  status TEXT CHECK (status IN ('passed', 'failed', 'pending', 'running')),
  duration_ms INTEGER,
  created_at TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE public.testing_explorer IS 'Stores test results for AI prompt generation validation';
COMMENT ON COLUMN public.testing_explorer.test_name IS 'Name of the test case';
COMMENT ON COLUMN public.testing_explorer.status IS 'Test status: passed, failed, pending, running';
COMMENT ON COLUMN public.testing_explorer.duration_ms IS 'Test execution duration in milliseconds';

CREATE INDEX IF NOT EXISTS idx_testing_explorer_test_name ON public.testing_explorer(test_name);
CREATE INDEX IF NOT EXISTS idx_testing_explorer_status ON public.testing_explorer(status);
CREATE INDEX IF NOT EXISTS idx_testing_explorer_created_at ON public.testing_explorer(created_at);

ALTER TABLE public.testing_explorer ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "testing_select_public" ON public.testing_explorer;
CREATE POLICY "testing_select_public" ON public.testing_explorer
  FOR SELECT USING (true);

DROP POLICY IF EXISTS "testing_insert_public" ON public.testing_explorer;
CREATE POLICY "testing_insert_public" ON public.testing_explorer
  FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "testing_update_public" ON public.testing_explorer;
CREATE POLICY "testing_update_public" ON public.testing_explorer
  FOR UPDATE USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "testing_delete_public" ON public.testing_explorer;
CREATE POLICY "testing_delete_public" ON public.testing_explorer
  FOR DELETE USING (true);
