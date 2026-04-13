// @handoff: 小花 (请集成到项目中)
// TICKET_BE-001: 登录系统 Auth API (Cloudflare Worker)
// 创建时间: 2026-04-11
//
// 路由:
//   POST /api/login  → 生成登录 token (调试模式直接返回)
//   POST /api/verify → 校验 token 有效性
//
// 环境变量 (通过 wrangler.toml 绑定):
//   env.DB → D1 数据库实例

// ---------- 工具函数 ----------

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function generateUUID() {
  return crypto.randomUUID();
}

function nowSeconds() {
  return Math.floor(Date.now() / 1000);
}

// ---------- 路由处理 ----------

/**
 * POST /api/login
 * 请求体: { "email": "user@example.com" }
 * 响应:   { "success": true, "token": "<uuid>" }
 *
 * 调试模式: 不校验 email，直接生成 token 返回。
 * 生产模式: 需要写入 users 表（upsert），再写入 login_tokens。
 */
async function handleLogin(env, request) {
  let email = '';
  try {
    const body = await request.json();
    email = body.email || '';
  } catch {
    // 调试模式：允许空 body
  }

  const token = generateUUID();
  const expiresAt = nowSeconds() + 15 * 60; // 15 分钟后过期

  try {
    // 写入 login_tokens
    await env.DB.prepare(
      'INSERT INTO login_tokens (token, user_email, expires_at, used) VALUES (?, ?, ?, 0)'
    ).bind(token, email, expiresAt).run();

    // 如果 email 非空，upsert 到 users 表
    if (email) {
      await env.DB.prepare(
        'INSERT INTO users (id, email, role) VALUES (?, ?, ?) ON CONFLICT(email) DO UPDATE SET role = role'
      ).bind(generateUUID(), email, 'user').run();
    }

    return jsonResponse({ success: true, token });
  } catch (err) {
    return jsonResponse({ success: false, error: err.message }, 500);
  }
}

/**
 * POST /api/verify
 * 请求体: { "token": "<uuid>" }
 * 响应成功: { "success": true, "email": "user@example.com" }
 * 响应失败: { "success": false, "error": "..." }
 */
async function handleVerify(env, request) {
  let token = '';
  try {
    const body = await request.json();
    token = body.token || '';
  } catch {
    return jsonResponse({ success: false, error: '无效的请求体' }, 400);
  }

  if (!token) {
    return jsonResponse({ success: false, error: '缺少 token' }, 400);
  }

  try {
    const result = await env.DB.prepare(
      'SELECT user_email, expires_at, used FROM login_tokens WHERE token = ?'
    ).bind(token).first();

    if (!result) {
      return jsonResponse({ success: false, error: 'token 不存在' }, 401);
    }

    if (result.used === 1) {
      return jsonResponse({ success: false, error: 'token 已被使用' }, 401);
    }

    if (result.expires_at < nowSeconds()) {
      return jsonResponse({ success: false, error: 'token 已过期' }, 401);
    }

    // 标记 token 为已使用
    await env.DB.prepare(
      'UPDATE login_tokens SET used = 1 WHERE token = ?'
    ).bind(token).run();

    return jsonResponse({ success: true, email: result.user_email });
  } catch (err) {
    return jsonResponse({ success: false, error: err.message }, 500);
  }
}

// ---------- CORS 预检 ----------

function handleCORS() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}

function addCorsHeaders(response) {
  response.headers.set('Access-Control-Allow-Origin', '*');
  response.headers.set('Access-Control-Allow-Methods', 'POST, OPTIONS');
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type');
  return response;
}

// ---------- 主入口 ----------

export default {
  async fetch(request, env, ctx) {
    // CORS 预检
    if (request.method === 'OPTIONS') {
      return handleCORS();
    }

    // 仅接受 POST
    if (request.method !== 'POST') {
      return jsonResponse({ error: 'Method Not Allowed' }, 405);
    }

    const url = new URL(request.url);
    const path = url.pathname;

    // 路由分发
    if (path === '/api/login') {
      return addCorsHeaders(await handleLogin(env, request));
    }

    if (path === '/api/verify') {
      return addCorsHeaders(await handleVerify(env, request));
    }

    // 404
    return addCorsHeaders(
      jsonResponse({ error: 'Not Found', path }, 404)
    );
  },
};
