import { Pool } from 'pg';

// Create a singleton connection pool
let pool: Pool | null = null;

export function getPool(): Pool {
  if (!pool) {
    // Strip sslmode parameter from connection string to prevent it from overriding our SSL config
    const connectionString = process.env.POSTGRES_URL?.replace(/[?&]sslmode=\w+/, '') || '';

    pool = new Pool({
      connectionString,
      ssl: {
        rejectUnauthorized: false, // DigitalOcean requires SSL but with self-signed cert
      },
    });
  }
  return pool;
}

// Helper function for easier query execution
export async function query(text: string, params?: any[]) {
  const pool = getPool();
  return pool.query(text, params);
}
