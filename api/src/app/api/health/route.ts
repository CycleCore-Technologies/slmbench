import { NextResponse } from 'next/server';
import { query } from '@/lib/db';

export async function GET() {
  try {
    // Test database connection
    const result = await query('SELECT NOW() as current_time, version() as pg_version');

    return NextResponse.json({
      status: 'healthy',
      database: 'connected',
      timestamp: result.rows[0].current_time,
      postgresVersion: result.rows[0].pg_version,
      environment: {
        nodeVersion: process.version,
        hasPostgresUrl: !!process.env.POSTGRES_URL,
        postgresUrlPrefix: process.env.POSTGRES_URL?.substring(0, 20) + '...',
      }
    });
  } catch (error: any) {
    console.error('Health check failed:', error);
    return NextResponse.json({
      status: 'unhealthy',
      error: error.message,
      code: error.code,
      stack: error.stack,
      environment: {
        nodeVersion: process.version,
        hasPostgresUrl: !!process.env.POSTGRES_URL,
        postgresUrlPrefix: process.env.POSTGRES_URL?.substring(0, 20) + '...',
      }
    }, { status: 500 });
  }
}
