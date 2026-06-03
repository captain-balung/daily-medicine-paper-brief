import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY;

export function createSupabaseClient() {
  if (!supabaseUrl || !supabaseKey) {
    throw new Error("Supabase public environment variables are missing.");
  }

  return createClient(supabaseUrl, supabaseKey);
}
