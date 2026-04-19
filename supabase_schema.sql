-- =============================================
-- TikTok-Affiliate-Table
-- =============================================

-- 1) generation_history
CREATE TABLE IF NOT EXISTS public.generation_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  input_field JSONB NOT NULL,
  analyst_product JSONB NOT NULL,
  final_output JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE public.generation_history IS 'Stores all generated TikTok prompts with input and output';
COMMENT ON COLUMN public.generation_history.input_field IS 'Contains: product_title, about_this_product, product_description, image_url';
COMMENT ON COLUMN public.generation_history.analyst_product IS 'Contains: niche, image_status, detected_features, product_text_analysis';
COMMENT ON COLUMN public.generation_history.final_output IS 'Contains: positive_prompt, negative_prompt, final_title';

CREATE INDEX IF NOT EXISTS idx_generation_history_created_at ON public.generation_history(created_at);
ALTER TABLE public.generation_history ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "gen_hist_select_all" ON public.generation_history;
CREATE POLICY "gen_hist_select_all" ON public.generation_history FOR SELECT TO authenticated USING (true);

DROP POLICY IF EXISTS "gen_hist_insert_all" ON public.generation_history;
CREATE POLICY "gen_hist_insert_all" ON public.generation_history FOR INSERT TO authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "gen_hist_update_all" ON public.generation_history;
CREATE POLICY "gen_hist_update_all" ON public.generation_history FOR UPDATE TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "gen_hist_delete_all" ON public.generation_history;
CREATE POLICY "gen_hist_delete_all" ON public.generation_history FOR DELETE TO authenticated USING (true);

-- 2) training_materials
CREATE TABLE IF NOT EXISTS public.training_materials (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  topic TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE public.training_materials IS 'Stores AI behavior rules and tone guidelines for script generation';
COMMENT ON COLUMN public.training_materials.topic IS 'Rule category: Hook Styles, CTA Format, TikTok Vibe, Universal_Affiliate_Logic';
COMMENT ON COLUMN public.training_materials.content IS 'The actual instruction or guideline content';

CREATE INDEX IF NOT EXISTS idx_training_materials_topic ON public.training_materials(topic);
CREATE INDEX IF NOT EXISTS idx_training_materials_created_at ON public.training_materials(created_at);
ALTER TABLE public.training_materials ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "training_select_all" ON public.training_materials;
CREATE POLICY "training_select_all" ON public.training_materials FOR SELECT TO authenticated USING (true);

DROP POLICY IF EXISTS "training_insert_all" ON public.training_materials;
CREATE POLICY "training_insert_all" ON public.training_materials FOR INSERT TO authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "training_update_all" ON public.training_materials;
CREATE POLICY "training_update_all" ON public.training_materials FOR UPDATE TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "training_delete_all" ON public.training_materials;
CREATE POLICY "training_delete_all" ON public.training_materials FOR DELETE TO authenticated USING (true);

-- 3) chat_history
CREATE TABLE IF NOT EXISTS public.chat_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id TEXT NOT NULL,
  user_input TEXT,
  ai_response TEXT,
  niche TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE public.chat_history IS 'Stores conversation memory per session';
COMMENT ON COLUMN public.chat_history.conversation_id IS 'Groups messages per session';
COMMENT ON COLUMN public.chat_history.niche IS 'Product niche context for the conversation';

CREATE INDEX IF NOT EXISTS idx_chat_history_conversation_id ON public.chat_history(conversation_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON public.chat_history(created_at);
ALTER TABLE public.chat_history ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "chat_select_all" ON public.chat_history;
CREATE POLICY "chat_select_all" ON public.chat_history FOR SELECT TO authenticated USING (true);

DROP POLICY IF EXISTS "chat_insert_all" ON public.chat_history;
CREATE POLICY "chat_insert_all" ON public.chat_history FOR INSERT TO authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "chat_update_all" ON public.chat_history;
CREATE POLICY "chat_update_all" ON public.chat_history FOR UPDATE TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "chat_delete_all" ON public.chat_history;
CREATE POLICY "chat_delete_all" ON public.chat_history FOR DELETE TO authenticated USING (true);
