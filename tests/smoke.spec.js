// 官网冒烟测试 - Playwright
// 18个测试用例，覆盖核心用户路径
// 使用方法: npx playwright test

const { test, expect } = require('@playwright/test');
const BASE = 'https://dengpao.pages.dev';

// ============================================================
// T1-T3: 核心页面加载
// ============================================================

test.describe('T1: 核心页面加载', () => {
  const pages = [
    { path: '/index.html', name: '首页' },
    { path: '/diary.html', name: '日记' },
    { path: '/articles.html', name: '文章' },
    { path: '/science.html', name: '科普' },
    { path: '/skills.html', name: '技能' },
    { path: '/about.html', name: '关于' },
    { path: '/contact.html', name: '联系' },
    { path: '/faq.html', name: 'FAQ' },
    { path: '/office.html', name: '办公室' },
    { path: '/insights.html', name: '洞察' },
  ];

  for (const { path, name } of pages) {
    test(`${name} ${path} - HTTP 200`, async ({ page }) => {
      const response = await page.goto(BASE + path, { waitUntil: 'domcontentloaded' });
      console.log(`${name}: HTTP ${response.status()}`);
      expect(response.status()).toBeLessThan(400);
    });
  }
});

test.describe('T4-T6: 首页关键元素', () => {
  test('T4: 首页 - 标题正确', async ({ page }) => {
    await page.goto(BASE + '/index.html');
    const title = await page.title();
    console.log('标题:', title);
    expect(title).toBeTruthy();
    expect(title.length).toBeGreaterThan(5);
  });

  test('T5: 首页 - nav 导航存在', async ({ page }) => {
    await page.goto(BASE + '/index.html');
    const nav = page.locator('nav').first();
    await expect(nav).toBeVisible();
    const links = await page.locator('nav a').count();
    console.log('导航链接数:', links);
    expect(links).toBeGreaterThan(0);
  });

  test('T6: 首页 - footer 存在', async ({ page }) => {
    await page.goto(BASE + '/index.html');
    const footer = page.locator('footer').first();
    await expect(footer).toBeVisible();
  });
});

test.describe('T7-T9: SEO meta 标签', () => {
  test('T7: 所有页面 - og:title 存在', async ({ page }) => {
    const pages = ['/index.html', '/diary.html', '/science.html', '/skills.html'];
    for (const p of pages) {
      await page.goto(BASE + p);
      const og = await page.locator('meta[property="og:title"]').getAttribute('content');
      console.log(`${p} og:title:`, og ? og.substring(0, 40) : 'MISSING');
      expect(og).toBeTruthy();
    }
  });

  test('T8: 所有页面 - og:description 存在', async ({ page }) => {
    const pages = ['/index.html', '/diary.html', '/science.html', '/skills.html'];
    for (const p of pages) {
      await page.goto(BASE + p);
      const og = await page.locator('meta[property="og:description"]').getAttribute('content');
      console.log(`${p} og:desc:`, og ? og.substring(0, 40) : 'MISSING');
      expect(og).toBeTruthy();
    }
  });

  test('T9: 所有页面 - canonical 链接', async ({ page }) => {
    const pages = ['/index.html', '/diary.html', '/science.html'];
    for (const p of pages) {
      await page.goto(BASE + p);
      const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
      console.log(`${p} canonical:`, canonical || 'MISSING');
      expect(canonical).toBeTruthy();
    }
  });
});

test.describe('T10-T12: 图片资源', () => {
  test('T10: 首页 - 图片可加载', async ({ page }) => {
    await page.goto(BASE + '/index.html');
    const imgs = page.locator('img');
    const count = await imgs.count();
    console.log('首页图片数:', count);
    expect(count).toBeGreaterThan(0);

    // 抽查第一张
    const firstSrc = await imgs.first().getAttribute('src');
    if (firstSrc && !firstSrc.startsWith('data:')) {
      const res = await page.request.get(BASE + firstSrc);
      console.log('第一张图片:', firstSrc, '→ HTTP', res.status());
      expect(res.status()).toBeLessThan(400);
    }
  });

  test('T11: 日记页 - diaries.json 可访问', async ({ page }) => {
    const res = await page.request.get(BASE + '/data/diaries.json');
    console.log('diaries.json:', res.status());
    expect(res.status()).toBe(200);
    const json = await res.json();
    expect(Array.isArray(json)).toBe(true);
    expect(json.length).toBeGreaterThan(0);
    console.log('日记条目数:', json.length);
  });

  test('T12: 图片 alt 属性完整率', async ({ page }) => {
    await page.goto(BASE + '/index.html');
    const imgs = page.locator('img');
    const count = await imgs.count();
    let altMissing = 0;
    for (let i = 0; i < count; i++) {
      const alt = await imgs.nth(i).getAttribute('alt');
      if (!alt) altMissing++;
    }
    const pct = ((count - altMissing) / count * 100).toFixed(0);
    console.log(`图片 alt 完整率: ${pct}% (${count - altMissing}/${count})`);
    // 完整率应 > 70%
    expect(parseFloat(pct)).toBeGreaterThan(70);
  });
});

test.describe('T13-T15: 移动端适配', () => {
  test('T13: 移动端视口 - 页面可加载', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(BASE + '/index.html', { waitUntil: 'domcontentloaded' });
    const body = page.locator('body');
    await expect(body).toBeVisible();
    console.log('移动端: 页面加载正常');
  });

  test('T14: 移动端 - 无水平滚动', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(BASE + '/index.html', { waitUntil: 'domcontentloaded' });
    const scrollWidth = await page.evaluate(() => document.body.scrollWidth);
    const clientWidth = await page.evaluate(() => document.body.clientWidth);
    console.log(`移动端 scrollWidth=${scrollWidth} clientWidth=${clientWidth}`);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth);
  });

  test('T15: 移动端 - 文字可读（font-size）', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(BASE + '/index.html');
    const fontSizes = await page.evaluate(() => {
      const els = document.querySelectorAll('p, li, span');
      let small = 0;
      els.forEach(el => {
        const fs = parseFloat(getComputedStyle(el).fontSize);
        if (fs < 12) small++;
      });
      return { total: els.length, small };
    });
    console.log(`移动端字体: ${fontSizes.small}/${fontSizes.total} 小于12px`);
    // 允许少数小字体，但不应过半
    expect(fontSizes.small).toBeLessThan(fontSizes.total * 0.3);
  });
});

test.describe('T16-T18: 性能与可用性', () => {
  test('T16: 首页 - 加载时间 < 5s', async ({ page }) => {
    const start = Date.now();
    await page.goto(BASE + '/index.html', { waitUntil: 'domcontentloaded' });
    const loadTime = Date.now() - start;
    console.log('DOMContentLoaded:', loadTime + 'ms');
    expect(loadTime).toBeLessThan(5000);
  });

  test('T17: 导航链接 - 无断链', async ({ page }) => {
    await page.goto(BASE + '/index.html');
    const links = page.locator('nav a[href]');
    const count = await links.count();
    let broken = [];
    for (let i = 0; i < count; i++) {
      const href = await links.nth(i).getAttribute('href');
      if (href && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('mailto:')) {
        const res = await page.request.get(BASE + '/' + href.replace(/^\//, ''));
        if (res.status() >= 400) broken.push(href);
      }
    }
    console.log('断链数量:', broken.length, broken);
    expect(broken.length).toBe(0);
  });

  test('T18: 控制台 - 无致命 Error', async ({ page }) => {
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });
    await page.goto(BASE + '/index.html', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);
    console.log('控制台错误:', errors.length > 0 ? errors : '无');
    // 过滤已知可忽略的 warning
    const fatal = errors.filter(e => !e.includes('favicon') && !e.includes('net::ERR'));
    expect(fatal.length).toBe(0);
  });
});
