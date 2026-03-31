# Lighthouse 基准测试

## 最新实测（2026-03-31 17:17）

**URL**: https://dengpao.pages.dev/
**工具**: Lighthouse 13.0.3 (CLI, headless Chrome)
**网络**: 本地直连（未开启节流）

---

## 评分对比

| 维度 | 01:14 (旧) | 17:17 (新) | 变化 |
|------|-----------|-----------|------|
| Performance | 55% | **62%** | ↑ +7 |
| Accessibility | 96% | **60%** | ↓↓ -36 |
| Best Practices | 100% | **96%** | ↓ -4 |
| SEO | 100% | **100%** | — |

> ⚠️ Accessibility 从 96% 暴跌至 60%，需立即排查

---

## 核心指标

| 指标 | 数值 | 评估 | 目标 |
|------|------|------|------|
| FCP | 3.0s | 🟡 偏慢 | < 1.8s |
| LCP | 8.3s | 🔴 差 | < 2.5s |
| TBT | 0ms | 🟢 良好 | < 200ms |
| Speed Index | 8.7s | 🔴 差 | < 3.4s |
| CLS | 0.032 | 🟢 良好 | < 0.1 |

> 注：上次 FCP 21.0s 可能是 Lighthouse 节流模拟导致，本次无节流为 3.0s

---

## Top Opportunities（可优化项）

| 优先级 | 项目 | 节省 |
|--------|------|------|
| 🔴 P1 | unused-css-rules（未使用CSS） | **1050ms** |
| 🟡 P2 | unminified-css（未压缩CSS） | **210ms** |

---

## Accessibility 问题清单（60%）

| 问题 | 分数 | 说明 |
|------|------|------|
| button-name | 0% | 按钮无 accessible name |
| color-contrast | 0% | 前景背景对比度不足 |
| landmark-one-main | 0% | 文档无 main landmark |
| listitem | 0% | li 未包裹在 ul/ol 内 |
| target-size | 0% | 触控目标尺寸不足 |
| link-in-text-block | 0% | 链接仅靠颜色区分 |

**Console Errors:**
1. `Failed to load resource: net::ERR_TIMED_OUT`
2. `Failed to load resource: the server responded with a status of 405`

---

## 下次优化目标

- [ ] Accessibility 从 60% 提升至 90%+
- [ ] LCP 从 8.3s 降至 < 4s（图片优化）
- [ ] Performance 从 62% 提升至 75%+
