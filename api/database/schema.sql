-- SLMBench Evaluation Service Database Schema
-- For DigitalOcean Managed PostgreSQL

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Evaluation Orders Table
CREATE TABLE evaluation_orders (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  stripe_session_id VARCHAR(255) UNIQUE NOT NULL,
  stripe_payment_intent_id VARCHAR(255),

  -- Customer Information
  email VARCHAR(255) NOT NULL,
  customer_name VARCHAR(255),

  -- Order Details
  product_type VARCHAR(50) NOT NULL, -- 'single', 'pack', 'enterprise'
  amount_cents INTEGER NOT NULL,
  currency VARCHAR(3) DEFAULT 'usd',

  -- Model Submission
  model_name VARCHAR(255) NOT NULL,
  huggingface_url TEXT NOT NULL,
  model_file_url TEXT,

  -- Status Tracking
  payment_status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'paid', 'failed'
  evaluation_status VARCHAR(50) DEFAULT 'queued', -- 'queued', 'running', 'completed', 'failed'

  -- Results
  results_json JSONB,
  report_url TEXT,
  certificate_url TEXT,

  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  paid_at TIMESTAMP,
  completed_at TIMESTAMP,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for Evaluation Orders
CREATE INDEX idx_evaluation_orders_email ON evaluation_orders(email);
CREATE INDEX idx_evaluation_orders_payment_status ON evaluation_orders(payment_status);
CREATE INDEX idx_evaluation_orders_evaluation_status ON evaluation_orders(evaluation_status);
CREATE INDEX idx_evaluation_orders_stripe_session ON evaluation_orders(stripe_session_id);
CREATE INDEX idx_evaluation_orders_created_at ON evaluation_orders(created_at DESC);

-- Enterprise Subscriptions Table
CREATE TABLE enterprise_subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  stripe_subscription_id VARCHAR(255) UNIQUE NOT NULL,
  stripe_customer_id VARCHAR(255) NOT NULL,

  -- Customer Information
  email VARCHAR(255) NOT NULL,
  company_name VARCHAR(255),

  -- Subscription Status
  status VARCHAR(50) DEFAULT 'active', -- 'active', 'canceled', 'past_due', 'incomplete'
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,

  -- Usage Tracking
  evaluations_this_month INTEGER DEFAULT 0,
  evaluations_total INTEGER DEFAULT 0,
  api_key VARCHAR(255) UNIQUE,

  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  canceled_at TIMESTAMP
);

-- Indexes for Enterprise Subscriptions
CREATE INDEX idx_enterprise_subscriptions_stripe_customer ON enterprise_subscriptions(stripe_customer_id);
CREATE INDEX idx_enterprise_subscriptions_status ON enterprise_subscriptions(status);
CREATE INDEX idx_enterprise_subscriptions_email ON enterprise_subscriptions(email);
CREATE INDEX idx_enterprise_subscriptions_api_key ON enterprise_subscriptions(api_key);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for automatic updated_at
CREATE TRIGGER update_evaluation_orders_updated_at
  BEFORE UPDATE ON evaluation_orders
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_enterprise_subscriptions_updated_at
  BEFORE UPDATE ON enterprise_subscriptions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Example queries for testing

-- View all pending evaluations
-- SELECT * FROM evaluation_orders WHERE payment_status = 'paid' AND evaluation_status = 'queued';

-- View all active enterprise subscriptions
-- SELECT * FROM enterprise_subscriptions WHERE status = 'active';

-- Check evaluation status for a specific order
-- SELECT id, model_name, payment_status, evaluation_status, created_at FROM evaluation_orders WHERE id = 'your-order-id';
