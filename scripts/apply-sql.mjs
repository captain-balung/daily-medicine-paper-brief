import { readFile } from "node:fs/promises";
import { Client } from "pg";

function parseEnv(text) {
  const env = {};

  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) {
      continue;
    }

    const equalsIndex = line.indexOf("=");
    if (equalsIndex === -1) {
      continue;
    }

    const key = line.slice(0, equalsIndex).trim();
    let value = line.slice(equalsIndex + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    env[key] = value;
  }

  return env;
}

const sqlFile = process.argv[2];
if (!sqlFile) {
  console.error("Usage: node scripts/apply-sql.mjs <sql-file>");
  process.exit(1);
}

const localEnv = parseEnv(await readFile(".env", "utf8"));
const databaseUrl = localEnv.DATABASE_URL ?? process.env.DATABASE_URL;

if (!databaseUrl) {
  console.error("DATABASE_URL is missing.");
  process.exit(1);
}

const sql = await readFile(sqlFile, "utf8");
const client = new Client({
  connectionString: databaseUrl,
  ssl: { rejectUnauthorized: false },
});

await client.connect();
try {
  await client.query(sql);
  console.log(`applied=${sqlFile}`);
} finally {
  await client.end();
}
