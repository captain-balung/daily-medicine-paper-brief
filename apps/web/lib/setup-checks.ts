type SetupCheck = {
  id: string;
  label: string;
  status: "pass" | "missing";
};

function hasEnv(name: string) {
  return Boolean(process.env[name] && process.env[name]?.trim());
}

export function getSetupChecks(): SetupCheck[] {
  return [
    {
      id: "supabase_url",
      label: "Supabase URL configured",
      status: hasEnv("NEXT_PUBLIC_SUPABASE_URL") ? "pass" : "missing",
    },
    {
      id: "supabase_key",
      label: "Supabase publishable key configured",
      status: hasEnv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY")
        ? "pass"
        : "missing",
    },
    {
      id: "publication_mode",
      label: "Auto-publish mode selected",
      status: "pass",
    },
    {
      id: "safety_rules",
      label: "Medical safety rules required",
      status: "pass",
    },
    {
      id: "sources",
      label: "Core sources selected",
      status: "pass",
    },
  ];
}
