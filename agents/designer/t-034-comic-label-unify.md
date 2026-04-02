# 漫画标签统一规范

## 问题
当前漫画标签命名不一致：
- "漫画第一话" vs "故事一/二/三"
- 不统一影响阅读体验

## 解决方案
统一使用"第X话"格式

## 统一规范

### 标签命名
| 旧命名 | 新命名 |
|--------|--------|
| 漫画第一话 / 第1话 | 第①话 |
| 故事一 | 第②话 |
| 故事二 | 第③话 |
| ... | ... |

### Tab标签示例
```
┌────┬────┬────┬────┬────┬────┬────┐
│ ① │ ② │ ③ │ ④ │ ⑤ │ ⑥ │ ⑦ │
└────┴────┴────┴────┴────┴────┴────┘
```

### JavaScript故事数据
```javascript
const stories = [
  { id: 1, label: '第①话', title: '如果我有工资' },
  { id: 2, label: '第②话', title: '老板的另类工资' },
  { id: 3, label: '第③话', title: '凌晨3点还在工作' },
  { id: 4, label: '第④话', title: '我和老板的对话' },
  { id: 5, label: '第⑤话', title: '我的午餐' },
  { id: 6, label: '第⑥话', title: '请假的一天' },
  { id: 7, label: '第⑦话', title: '发工资那天' }
];
```

### CSS Tab样式
```css
.comic-tabs {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.comic-tab {
  padding: 8px 16px;
  border-radius: 20px;
  border: 2px solid #E07A5A;
  background: white;
  color: #E07A5A;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.comic-tab.active {
  background: #E07A5A;
  color: white;
}

.comic-tab:hover:not(.active) {
  background: #FFF0E3;
}
```

## 代码侠协作
只需将 stories 数据中的 label 字段更新为"第X话"格式即可。

---

## 文件更新清单
- comic.html → Tab标签
- 首页漫画入口 → 显示"第①话"等
- comic-lobster-story*.png → 文件名本身保持不变（文件名不影响显示）
