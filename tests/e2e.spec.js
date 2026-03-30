// Playwright E2E 测试配置
// 使用方法: npx playwright test

const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 30000,
  use: {
    // 测试环境 URL
    baseURL: 'https://dengpao.pages.dev',
    // 截图保存
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    // 桌面
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
    // 移动端模拟
    {
      name: 'mobile',
      use: {
        browserName: 'chromium',
        viewport: { width: 375, height: 667 },
      },
    },
  ],
});
