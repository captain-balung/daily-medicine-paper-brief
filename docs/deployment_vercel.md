# Vercel Deployment

## Import Project

1. Import the GitHub repository into Vercel.
2. Use the repository root as the Vercel project root.
3. Vercel will use `vercel.json`.

## Environment Variables

Set these in Vercel Project Settings:

```env
NEXT_PUBLIC_SUPABASE_URL=https://fkucugazszaugtfvbvzr.supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=
```

Only public Supabase variables are required for the web app.

Do not add backend secrets to Vercel for this MVP web deployment:

```env
SUPABASE_SECRET_KEY
DATABASE_URL
ANTHROPIC_API_KEY
```

Those are for local/Render worker only.

## Current MVP Behavior

- Public pages read published daily briefings through Supabase RLS.
- Pipeline jobs still run locally for now.
- Render deployment comes after the web preview is reviewed.
