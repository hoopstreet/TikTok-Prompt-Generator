-- =============================================
-- Enable public access for development
-- Run this in Supabase SQL Editor if needed
-- =============================================

-- Drop existing policies for generation_history
DROP POLICY IF EXISTS "gen_hist_select_all" ON public.generation_history;
DROP POLICY IF EXISTS "gen_hist_insert_all" ON public.generation_history;
DROP POLICY IF EXISTS "gen_hist_update_all" ON public.generation_history;
DROP POLICY IF EXISTS "gen_hist_delete_all" ON public.generation_history;

-- Create public access policies (no authentication required)
CREATE POLICY "gen_hist_select_public" ON public.generation_history
    FOR SELECT USING (true);

CREATE POLICY "gen_hist_insert_public" ON public.generation_history
    FOR INSERT WITH CHECK (true);

-- Drop existing policies for training_materials
DROP POLICY IF EXISTS "training_select_all" ON public.training_materials;
DROP POLICY IF EXISTS "training_insert_all" ON public.training_materials;
DROP POLICY IF EXISTS "training_update_all" ON public.training_materials;
DROP POLICY IF EXISTS "training_delete_all" ON public.training_materials;

-- Create public access policies for training_materials
CREATE POLICY "training_select_public" ON public.training_materials
    FOR SELECT USING (true);

CREATE POLICY "training_insert_public" ON public.training_materials
    FOR INSERT WITH CHECK (true);

-- Drop existing policies for chat_history
DROP POLICY IF EXISTS "chat_select_all" ON public.chat_history;
DROP POLICY IF EXISTS "chat_insert_all" ON public.chat_history;
DROP POLICY IF EXISTS "chat_update_all" ON public.chat_history;
DROP POLICY IF EXISTS "chat_delete_all" ON public.chat_history;

-- Create public access policies for chat_history
CREATE POLICY "chat_select_public" ON public.chat_history
    FOR SELECT USING (true);

CREATE POLICY "chat_insert_public" ON public.chat_history
    FOR INSERT WITH CHECK (true);

CREATE POLICY "chat_update_public" ON public.chat_history
    FOR UPDATE USING (true);

CREATE POLICY "chat_delete_public" ON public.chat_history
    FOR DELETE USING (true);

-- Verify policies
SELECT tablename, policyname, permissive, roles, cmd
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
