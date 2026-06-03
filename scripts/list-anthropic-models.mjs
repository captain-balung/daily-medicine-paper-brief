import { readFile } from "node:fs/promises";

function parseEnv(text) {
  const env = {};

  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#") || !line.includes("=")) continue;
    const [key, ...rest] = line.split("=");
    let value = rest.join("=").trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    env[key.trim()] = value;
  }

  return env;
}

const env = parseEnv(await readFile(".env", "utf8"));
const apiKey = env.ANTHROPIC_API_KEY ?? process.env.ANTHROPIC_API_KEY;
if (!apiKey) {
  console.error("ANTHROPIC_API_KEY is missing.");
  process.exit(1);
}

const response = await fetch("https://api.anthropic.com/v1/models", {
  headers: {
    "x-api-key": apiKey,
    "anthropic-version": "2023-06-01",
  },
});

const payload = await response.json();
if (!response.ok) {
  console.error(JSON.stringify(payload, null, 2));
  process.exit(1);
}

console.log(
  JSON.stringify(
    (payload.data ?? []).map((model) => ({
      id: model.id,
      display_name: model.display_name,
      created_at: model.created_at,
    })),
    null,
    2,
  ),
);
