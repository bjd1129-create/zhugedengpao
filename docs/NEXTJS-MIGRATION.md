# Next.js 迁移评估报告

**评估日期:** 2026-04-10
**评估人:** 资深开发者

---

## 一、现状分析

### 当前架构

| 网站 | 技术栈 | 部署平台 | 日均访问 |
|------|--------|----------|----------|
| 官网 dengpao.pages.dev | 纯静态 HTML/CSS/JS | Cloudflare Pages | ~500 |
| 记忆网站 306alp.pages.dev | 纯静态 HTML/CSS/JS | Cloudflare Pages | ~200 |

### 优点

1. **极简架构** - 无框架依赖，首屏快
2. **部署简单** - Git push 即可部署
3. **成本低** - Cloudflare Pages 免费套餐足够
4. **维护容易** - 纯前端，无需后端服务

### 痛点

1. **SEO 局限** - 动态内容渲染受限
2. **组件复用** - 重复代码多
3. **状态管理** - 无统一状态管理
4. **开发体验** - 大项目难以维护

---

## 二、Next.js 迁移方案

### 方案对比

| 方案 | 优点 | 缺点 | 适合场景 |
|------|------|------|----------|
| **保持静态** | 简单、快速 | 扩展性差 | 内容固定、小型网站 |
| **SSR (App Router)** | SEO 最佳、动态能力 | 成本高、复杂度增加 | 内容更新频繁 |
| **SSG + ISR** | 静态性能 + 增量更新 | 需要 Vercel/CF | 内容更新频率中等 |
| **混合方案** | 灵活、按需渲染 | 配置复杂 | 复杂应用 |

### 推荐: SSG + ISR (Incremental Static Regeneration)

**理由:**
1. 保留静态网站的所有优点
2. 内容更新时自动重新生成
3. Vercel 或 Cloudflare Pages 都支持
4. 团队学习成本较低

---

## 三、迁移路线图

### Phase 1: 准备阶段 (第1周)

```
目标: 建立 Next.js 项目基础架构
```

```bash
# 创建项目
npx create-next-app@latest zhuge-dengpao-web
  --typescript
  --tailwind
  --eslint
  --app
  --src-dir
  --import-alias "@/*"

cd zhuge-dengpao-web

# 安装依赖
npm install lucide-react @radix-ui/react-icons
```

**目录结构设计:**

```
src/
├── app/
│   ├── (marketing)/           # 营销页面组
│   │   ├── page.tsx          # 首页
│   │   ├── about/page.tsx    # 关于
│   │   ├── pricing/page.tsx  # 价格
│   │   └── layout.tsx
│   ├── (app)/                # 应用页面组
│   │   ├── dashboard/page.tsx
│   │   └── layout.tsx
│   ├── api/                  # API Routes
│   │   └── comments/route.ts
│   ├── layout.tsx            # Root Layout
│   └── globals.css
├── components/
│   ├── ui/                   # 基础组件
│   ├── marketing/            # 营销组件
│   └── app/                  # 应用组件
├── lib/
│   ├── utils.ts
│   └── api.ts
└── types/
    └── index.ts
```

### Phase 2: 迁移首页 (第2周)

```
目标: 迁移官网首页，保持外观一致
```

**关键组件:**

```tsx
// app/(marketing)/page.tsx
import { Hero } from '@/components/marketing/hero';
import { Features } from '@/components/marketing/features';
import { Testimonials } from '@/components/marketing/testimonials';

export default function HomePage() {
  return (
    <main>
      <Hero />
      <Features />
      <Testimonials />
    </main>
  );
}
```

### Phase 3: 迁移其他页面 (第3周)

```
目标: 迁移所有静态页面
```

- pricing.html → app/(marketing)/pricing/page.tsx
- articles.html → app/(marketing)/articles/page.tsx
- about.html → app/(marketing)/about/page.tsx

### Phase 4: 性能优化 (第4周)

```
目标: 达成 Core Web Vitals 优秀标准
```

| 指标 | 目标 | 优化手段 |
|------|------|----------|
| LCP | < 2.5s | 图片优化、预加载 |
| FID | < 100ms | 代码分割、懒加载 |
| CLS | < 0.1 | 预留图片空间 |

---

## 四、组件库设计

### 设计系统 Token

```tsx
// lib/design-tokens.ts
export const tokens = {
  colors: {
    primary: '#4A2508',
    secondary: '#E5A853',
    background: '#f5f3ee',
    text: '#222',
    muted: '#888',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
  },
  radius: {
    sm: '4px',
    md: '8px',
    lg: '16px',
  },
} as const;
```

### 基础组件

| 组件 | 用途 |
|------|------|
| Button | 按钮 (primary/secondary/ghost) |
| Card | 卡片容器 |
| Input | 输入框 |
| Modal | 弹窗 |
| Badge | 标签 |
| Avatar | 头像 |

---

## 五、学习资源

### 官方文档
- [Next.js 14 App Router](https://nextjs.org/docs/app)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript](https://www.typescriptlang.org/docs/)

### 推荐学习路径

```
Week 1: TypeScript 基础 + React Hooks
Week 2: Next.js App Router 核心概念
Week 3: Tailwind CSS 组件开发
Week 4: API Routes + 数据库集成
Week 5: 性能优化 + 部署
```

---

## 六、风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 学习曲线 | 中 | 分阶段迁移，每周一个小目标 |
| SEO 波动 | 中 | 保持 URL 结构一致，设置 301 重定向 |
| 性能退化 | 低 | 使用 SSG，监控 Core Web Vitals |

---

## 七、决策点

在开始迁移前，请确认:

- [ ] 是否需要真正的动态功能？还是内容管理更方便？
- [ ] 团队是否愿意投入时间学习 Next.js？
- [ ] 是否需要 CMS 集成 (如 Sanity, Contentlayer)？
- [ ] 预算是否支持 Vercel Pro ($20/月) 或保持 Cloudflare Pages (免费)？

---

**建议:** 如果团队资源有限，建议保持当前静态架构，但将代码重构为组件化设计，为未来迁移做准备。

---

*资深开发者 | 2026-04-10*
