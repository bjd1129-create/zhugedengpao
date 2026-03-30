// 官网冒烟测试 - Playwright
// 测试关键用户路径

const { test, expect } = require('@playwright/test');

const BASE = 'https://dengpao.pages.dev';

test.describe('官网冒烟测试', () => {

  test('首页 - 加载正常', async ({ page }) => {
    await page.goto(BASE + '/');
    
    // 检查标题
    const title = await page.title();
    console.log('页面标题:', title);
    
    // 检查关键元素存在
    await expect(page.locator('body')).toBeVisible();
    
    // 检查没有致命错误（控制台）
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });
    
    await page.waitForTimeout(1000);
    console.log('控制台错误:', errors.length > 0 ? errors : '无');
  });

  test('导航 - 所有页面可访问', async ({ page }) => {
    const pages = [
      '/',
      '/about',
      '/science',
      '/skills',
      '/easyclaw',
      '/pricing',
      '/faq',
    ];
    
    for (const path of pages) {
      console.log('测试:', path);
      const response = await page.goto(BASE + path);
      expect(response.status()).toBeLessThan(400);
    }
  });

  test('首页 - 关键内容存在', async ({ page }) => {
    await page.goto(BASE + '/');
    
    // 检查导航
    const nav = page.locator('nav');
    await expect(nav).toBeVisible();
    
    // 检查 hero 区
    const hero = page.locator('header, .hero, .banner').first();
    await expect(hero).toBeVisible();
    
    // 检查 footer
    const footer = page.locator('footer');
    await expect(footer).toBeVisible();
  });

  test('SEO - 关键 meta 标签', async ({ page }) => {
    await page.goto(BASE + '/');
    
    // 检查 og:title
    const ogTitle = await page.locator('meta[property="og:title"]').getAttribute('content');
    console.log('og:title:', ogTitle);
    expect(ogTitle).toBeTruthy();
    
    // 检查 og:description
    const ogDesc = await page.locator('meta[property="og:description"]').getAttribute('content');
    console.log('og:description:', ogDesc ? ogDesc.substring(0, 50) + '...' : '缺失');
    expect(ogDesc).toBeTruthy();
    
    // 检查 canonical
    const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
    console.log('canonical:', canonical);
    expect(canonical).toBeTruthy();
  });

  test('移动端 - 响应式布局', async ({ page }) => {
    // 移动端视口
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(BASE + '/');
    
    // 检查页面可加载
    await expect(page.locator('body')).toBeVisible();
    
    // 如果有汉堡菜单，应该可见
    const navToggle = page.locator('.nav-toggle, .menu-toggle, [class*="hamburger"]');
    if (await navToggle.count() > 0) {
      console.log('移动端导航: 汉堡菜单存在');
    }
  });

  test('性能 - 页面加载时间', async ({ page }) => {
    const start = Date.now();
    await page.goto(BASE + '/');
    const loadTime = Date.now() - start;
    
    console.log('页面加载时间:', loadTime + 'ms');
    
    // 页面应在 5 秒内加载
    expect(loadTime).toBeLessThan(5000);
  });
});

test.describe('表单功能测试', () => {
  test('联系页面 - 表单元素存在', async ({ page }) => {
    await page.goto(BASE + '/contact');
    
    const form = page.locator('form');
    if (await form.count() > 0) {
      console.log('联系表单: 存在');
      await expect(form).toBeVisible();
    } else {
      console.log('联系表单: 不存在（可能用其他方式联系）');
    }
  });
});

test.describe('外部资源测试', () => {
  test('图片资源 - 可访问', async ({ page }) => {
    await page.goto(BASE + '/');
    
    const images = page.locator('img');
    const count = await images.count();
    console.log('图片数量:', count);
    
    // 抽查前 3 张图片
    for (let i = 0; i < Math.min(3, count); i++) {
      const img = images.nth(i);
      const src = await img.getAttribute('src');
      if (src && !src.startsWith('data:')) {
        console.log('检查图片:', src);
        const response = await page.request.get(BASE + src);
        expect(response.status()).toBeLessThan(400);
      }
    }
  });
});
