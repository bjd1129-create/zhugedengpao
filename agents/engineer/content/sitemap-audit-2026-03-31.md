# Sitemap URL 有效性抽检报告

**时间**：2026-03-31 00:37
**方法**：从 sitemap.xml 随机抽取10个URL，HTTP 状态码验证

---

## 抽检结果

| 状态码 | URL | 结果 |
|--------|-----|------|
| 200 | https://dengpao.pages.dev/ | ✅ |
| 200 | https://dengpao.pages.dev/diary | ✅ |
| 200 | https://dengpao.pages.dev/diary/day-0 | ✅ |
| 200 | https://dengpao.pages.dev/diary/day-10 | ✅ |
| 200 | https://dengpao.pages.dev/diary/day-22 | ✅ |
| 200 | https://dengpao.pages.dev/science | ✅ |
| 200 | https://dengpao.pages.dev/articles | ✅ |
| 200 | https://dengpao.pages.dev/office | ✅ |
| 200 | https://dengpao.pages.dev/pricing | ✅ |
| 200 | https://dengpao.pages.dev/article | ✅ |

**合格率**：10/10 = 100%

---

## 说明

- 所有 URL 均通过 `curl -L`（跟随重定向）检测
- sitemap.xml 共44个URL，包含 day-0 ~ day-23 全部日记页面
- 本次抽检未发现 404 / 301 / 302 等异常

---

## 待做

- [ ] 全量44个URL自动化扫描（Session 2 未完成项）
- [ ] 检测是否有外部链接指向不存在页面
