-- @handoff: 小花 (请集成到项目中)
-- TICKET_BE-001: 登录系统 D1 建表脚本
-- 创建时间: 2026-04-11
-- 执行方式: wrangler d1 execute dengpao-auth-db --file=schema.sql

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  role TEXT DEFAULT 'user',
  created_at INTEGER DEFAULT (strftime('%s', 'now'))
);

CREATE TABLE IF NOT EXISTS login_tokens (
  token TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  expires_at INTEGER NOT NULL,
  used INTEGER DEFAULT 0
);
