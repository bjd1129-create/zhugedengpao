# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## 网页截图工具配置

### 问题背景
Canvas工具报`node required`，无法直接截网页。

### 解决方案：playwright + chromium

**1. 安装playwright**
```bash
pip3 install playwright
# 或
pip install playwright
```

**2. 安装chromium浏览器**
```bash
python3 -m playwright install chromium
```

**3. 使用代理禁用+截图**
```python
import os
os.environ['no_proxy'] = '*'
os.environ['NO_PROXY'] = '*'

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(proxy=None)
    page = browser.new_page()
    page.goto('https://example.com', wait_until='domcontentloaded', timeout=60000)
    page.screenshot(path='/tmp/output.png', full_page=True)
    browser.close()
```

**4. 常见问题**
- Timeout：禁用代理重试
- 权限错误：检查chromium是否安装完整

### 经验总结
- Canvas工具不可用时，playwright是备选方案
- 需要先安装chromium
- 国内环境可能需要禁用代理

