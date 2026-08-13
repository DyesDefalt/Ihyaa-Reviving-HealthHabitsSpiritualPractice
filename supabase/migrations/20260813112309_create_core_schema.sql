/*
# Create Core Schema for Islamic Wellness Challenge App

1. New Tables

  - `profiles` — Extended user profile and preferences
    - `id` (uuid, PK, references auth.users)
    - `display_name` (text)
    - `fitness_level` (text) — beginner/intermediate/advanced
    - `health_goals` (text[]) — selected goals
    - `dietary_preferences` (text[]) — halal dietary specifics
    - `sleep_habit` (text) — early_bird/night_owl/moderate
    - `spiritual_level` (text) — beginner/practicing/devoted
    - `preferred_challenge` (text) — 30_days/100_days/1_year
    - `onboarding_completed` (boolean)
    - `points_balance` (integer)
    - `current_streak` (integer)
    - `longest_streak` (integer)
    - `timezone` (text)
    - `created_at` / `updated_at` (timestamptz)

  - `challenges` — Active challenge enrollments
    - `id` (uuid, PK)
    - `user_id` (uuid, FK to auth.users)
    - `challenge_type` (text) — 30_days/100_days/1_year
    - `status` (text) — active/paused/completed/abandoned
    - `start_date` (date)
    - `end_date` (date)
    - `current_day` (integer)
    - `created_at` / `updated_at` (timestamptz)

  - `daily_tasks` — Generated daily tasks for each challenge
    - `id` (uuid, PK)
    - `challenge_id` (uuid, FK to challenges)
    - `user_id` (uuid, FK to auth.users)
    - `day_number` (integer)
    - `scheduled_date` (date)
    - `pillar` (text) — physical/nutrition/mental/spiritual
    - `title` (text)
    - `description` (text)
    - `duration_minutes` (integer)
    - `quran_reference` (text)
    - `hadith_reference` (text)
    - `scientific_reference` (text)
    - `difficulty` (integer, 1-10)
    - `points_reward` (integer)
    - `completed` (boolean)
    - `completed_at` (timestamptz)

  - `daily_checkins` — Daily check-in reflections
    - `id` (uuid, PK)
    - `user_id` (uuid, FK to auth.users)
    - `challenge_id` (uuid, FK to challenges)
    - `checkin_date` (date)
    - `mood_rating` (integer, 1-5)
    - `energy_rating` (integer, 1-5)
    - `gratitude_note` (text)
    - `reflection_note` (text)
    - `tasks_completed` (integer)
    - `tasks_total` (integer)
    - `points_earned` (integer)

  - `point_transactions` — Points ledger
    - `id` (uuid, PK)
    - `user_id` (uuid, FK to auth.users)
    - `amount` (integer)
    - `type` (text) — earned/redeemed
    - `source` (text) — task_complete/streak_bonus/checkin/store_redeem
    - `description` (text)
    - `created_at` (timestamptz)

  - `store_items` — Rewards store items
    - `id` (uuid, PK)
    - `name` (text)
    - `description` (text)
    - `points_cost` (integer)
    - `category` (text)
    - `image_url` (text)
    - `is_active` (boolean)
    - `created_at` (timestamptz)

  - `store_redemptions` — User store purchases
    - `id` (uuid, PK)
    - `user_id` (uuid, FK to auth.users)
    - `store_item_id` (uuid, FK to store_items)
    - `points_spent` (integer)
    - `status` (text) — pending/fulfilled
    - `created_at` (timestamptz)

  - `knowledge_cards` — Weekly knowledge cards content
    - `id` (uuid, PK)
    - `title` (text)
    - `content` (text)
    - `quran_verse` (text)
    - `hadith_text` (text)
    - `scientific_fact` (text)
    - `category` (text)
    - `pillar` (text)
    - `created_at` (timestamptz)

2. Security
  - RLS enabled on ALL tables
  - Owner-scoped CRUD for user data tables
  - Public read for store_items and knowledge_cards
  - Authenticated-only write for user-specific tables

3. Important Notes
  - profiles.id references auth.users(id) directly (1:1)
  - points_balance on profiles is the authoritative balance
  - daily_checkins has unique constraint on (user_id, checkin_date) per challenge
*/

-- Profiles table (1:1 with auth.users)
CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name text,
  fitness_level text DEFAULT 'beginner',
  health_goals text[] DEFAULT '{}',
  dietary_preferences text[] DEFAULT '{}',
  sleep_habit text DEFAULT 'moderate',
  spiritual_level text DEFAULT 'beginner',
  preferred_challenge text DEFAULT '30_days',
  onboarding_completed boolean NOT NULL DEFAULT false,
  points_balance integer NOT NULL DEFAULT 0,
  current_streak integer NOT NULL DEFAULT 0,
  longest_streak integer NOT NULL DEFAULT 0,
  timezone text DEFAULT 'UTC',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "select_own_profile" ON profiles;
CREATE POLICY "select_own_profile" ON profiles FOR SELECT
  TO authenticated USING (auth.uid() = id);

DROP POLICY IF EXISTS "insert_own_profile" ON profiles;
CREATE POLICY "insert_own_profile" ON profiles FOR INSERT
  TO authenticated WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "update_own_profile" ON profiles;
CREATE POLICY "update_own_profile" ON profiles FOR UPDATE
  TO authenticated USING (auth.uid() = id) WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "delete_own_profile" ON profiles;
CREATE POLICY "delete_own_profile" ON profiles FOR DELETE
  TO authenticated USING (auth.uid() = id);

-- Challenges table
CREATE TABLE IF NOT EXISTS challenges (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL DEFAULT auth.uid() REFERENCES auth.users(id) ON DELETE CASCADE,
  challenge_type text NOT NULL DEFAULT '30_days',
  status text NOT NULL DEFAULT 'active',
  start_date date NOT NULL DEFAULT CURRENT_DATE,
  end_date date NOT NULL,
  current_day integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE challenges ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "select_own_challenges" ON challenges;
CREATE POLICY "select_own_challenges" ON challenges FOR SELECT
  TO authenticated USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "insert_own_challenges" ON challenges;
CREATE POLICY "insert_own_challenges" ON challenges FOR INSERT
  TO authenticated WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "update_own_challenges" ON challenges;
CREATE POLICY "update_own_challenges" ON challenges FOR UPDATE
  TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "delete_own_challenges" ON challenges;
CREATE POLICY "delete_own_challenges" ON challenges FOR DELETE
  TO authenticated USING (auth.uid() = user_id);

-- Daily tasks table
CREATE TABLE IF NOT EXISTS daily_tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  challenge_id uuid NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
  user_id uuid NOT NULL DEFAULT auth.uid() REFERENCES auth.users(id) ON DELETE CASCADE,
  day_number integer NOT NULL,
  scheduled_date date NOT NULL,
  pillar text NOT NULL,
  title text NOT NULL,
  description text NOT NULL DEFAULT '',
  duration_minutes integer NOT NULL DEFAULT 5,
  quran_reference text,
  hadith_reference text,
  scientific_reference text,
  difficulty integer NOT NULL DEFAULT 1,
  points_reward integer NOT NULL DEFAULT 10,
  completed boolean NOT NULL DEFAULT false,
  completed_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_daily_tasks_user_date ON daily_tasks(user_id, scheduled_date);
CREATE INDEX IF NOT EXISTS idx_daily_tasks_challenge ON daily_tasks(challenge_id, day_number);

ALTER TABLE daily_tasks ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "select_own_tasks" ON daily_tasks;
CREATE POLICY "select_own_tasks" ON daily_tasks FOR SELECT
  TO authenticated USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "insert_own_tasks" ON daily_tasks;
CREATE POLICY "insert_own_tasks" ON daily_tasks FOR INSERT
  TO authenticated WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "update_own_tasks" ON daily_tasks;
CREATE POLICY "update_own_tasks" ON daily_tasks FOR UPDATE
  TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "delete_own_tasks" ON daily_tasks;
CREATE POLICY "delete_own_tasks" ON daily_tasks FOR DELETE
  TO authenticated USING (auth.uid() = user_id);

-- Daily check-ins
CREATE TABLE IF NOT EXISTS daily_checkins (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL DEFAULT auth.uid() REFERENCES auth.users(id) ON DELETE CASCADE,
  challenge_id uuid NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
  checkin_date date NOT NULL DEFAULT CURRENT_DATE,
  mood_rating integer NOT NULL DEFAULT 3,
  energy_rating integer NOT NULL DEFAULT 3,
  gratitude_note text,
  reflection_note text,
  tasks_completed integer NOT NULL DEFAULT 0,
  tasks_total integer NOT NULL DEFAULT 0,
  points_earned integer NOT NULL DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE(user_id, challenge_id, checkin_date)
);

CREATE INDEX IF NOT EXISTS idx_checkins_user_date ON daily_checkins(user_id, checkin_date);

ALTER TABLE daily_checkins ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "select_own_checkins" ON daily_checkins;
CREATE POLICY "select_own_checkins" ON daily_checkins FOR SELECT
  TO authenticated USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "insert_own_checkins" ON daily_checkins;
CREATE POLICY "insert_own_checkins" ON daily_checkins FOR INSERT
  TO authenticated WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "update_own_checkins" ON daily_checkins;
CREATE POLICY "update_own_checkins" ON daily_checkins FOR UPDATE
  TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "delete_own_checkins" ON daily_checkins;
CREATE POLICY "delete_own_checkins" ON daily_checkins FOR DELETE
  TO authenticated USING (auth.uid() = user_id);

-- Point transactions
CREATE TABLE IF NOT EXISTS point_transactions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL DEFAULT auth.uid() REFERENCES auth.users(id) ON DELETE CASCADE,
  amount integer NOT NULL,
  type text NOT NULL DEFAULT 'earned',
  source text NOT NULL,
  description text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_points_user ON point_transactions(user_id, created_at);

ALTER TABLE point_transactions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "select_own_points" ON point_transactions;
CREATE POLICY "select_own_points" ON point_transactions FOR SELECT
  TO authenticated USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "insert_own_points" ON point_transactions;
CREATE POLICY "insert_own_points" ON point_transactions FOR INSERT
  TO authenticated WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "update_own_points" ON point_transactions;
CREATE POLICY "update_own_points" ON point_transactions FOR UPDATE
  TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "delete_own_points" ON point_transactions;
CREATE POLICY "delete_own_points" ON point_transactions FOR DELETE
  TO authenticated USING (auth.uid() = user_id);

-- Store items (publicly readable)
CREATE TABLE IF NOT EXISTS store_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  description text NOT NULL DEFAULT '',
  points_cost integer NOT NULL,
  category text NOT NULL DEFAULT 'general',
  image_url text,
  is_active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE store_items ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "anyone_can_read_store" ON store_items;
CREATE POLICY "anyone_can_read_store" ON store_items FOR SELECT
  TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "no_insert_store" ON store_items;
CREATE POLICY "no_insert_store" ON store_items FOR INSERT
  TO authenticated WITH CHECK (false);

DROP POLICY IF EXISTS "no_update_store" ON store_items;
CREATE POLICY "no_update_store" ON store_items FOR UPDATE
  TO authenticated USING (false) WITH CHECK (false);

DROP POLICY IF EXISTS "no_delete_store" ON store_items;
CREATE POLICY "no_delete_store" ON store_items FOR DELETE
  TO authenticated USING (false);

-- Store redemptions
CREATE TABLE IF NOT EXISTS store_redemptions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL DEFAULT auth.uid() REFERENCES auth.users(id) ON DELETE CASCADE,
  store_item_id uuid NOT NULL REFERENCES store_items(id),
  points_spent integer NOT NULL,
  status text NOT NULL DEFAULT 'pending',
  created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE store_redemptions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "select_own_redemptions" ON store_redemptions;
CREATE POLICY "select_own_redemptions" ON store_redemptions FOR SELECT
  TO authenticated USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "insert_own_redemptions" ON store_redemptions;
CREATE POLICY "insert_own_redemptions" ON store_redemptions FOR INSERT
  TO authenticated WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "update_own_redemptions" ON store_redemptions;
CREATE POLICY "update_own_redemptions" ON store_redemptions FOR UPDATE
  TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "delete_own_redemptions" ON store_redemptions;
CREATE POLICY "delete_own_redemptions" ON store_redemptions FOR DELETE
  TO authenticated USING (auth.uid() = user_id);

-- Knowledge cards (publicly readable)
CREATE TABLE IF NOT EXISTS knowledge_cards (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  content text NOT NULL DEFAULT '',
  quran_verse text,
  hadith_text text,
  scientific_fact text,
  category text NOT NULL DEFAULT 'general',
  pillar text NOT NULL DEFAULT 'spiritual',
  created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE knowledge_cards ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "anyone_can_read_knowledge" ON knowledge_cards;
CREATE POLICY "anyone_can_read_knowledge" ON knowledge_cards FOR SELECT
  TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "no_insert_knowledge" ON knowledge_cards;
CREATE POLICY "no_insert_knowledge" ON knowledge_cards FOR INSERT
  TO authenticated WITH CHECK (false);

DROP POLICY IF EXISTS "no_update_knowledge" ON knowledge_cards;
CREATE POLICY "no_update_knowledge" ON knowledge_cards FOR UPDATE
  TO authenticated USING (false) WITH CHECK (false);

DROP POLICY IF EXISTS "no_delete_knowledge" ON knowledge_cards;
CREATE POLICY "no_delete_knowledge" ON knowledge_cards FOR DELETE
  TO authenticated USING (false);
