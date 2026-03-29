// Playwright 配置文件
module.exports = {
  testDir: './tests',
  testMatch: '**/*.spec.js',
  timeout: 30000,
  retries: 1,
  workers: 2,
  use: {
    baseURL: 'https://dengpao.pages.dev',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'mobile', use: { browserName: 'chromium', viewport: { width: 375, height: 667 } } },
  ],
  webServer: undefined, // 不需要启动本地服务器，测试生产环境
};
